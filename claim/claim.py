import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel

async def check_user_level_permissions(ctx, permission_level = PermissionLevel.MODERATOR):
    if await ctx.bot.is_owner(ctx.author):
        # Bot owner(s) (and creator) has absolute power over the bot
        return True

    if (
        permission_level is not PermissionLevel.OWNER
        and ctx.channel.permissions_for(ctx.author).administrator
        and ctx.guild == ctx.bot.modmail_guild
    ):
        # Administrators have permission to all non-owner commands in the Modmail Guild
        return True

    level_permissions = ctx.bot.config["level_permissions"]
    checkables = {*ctx.author.roles, ctx.author}

    for level in PermissionLevel:
        if level >= permission_level and level.name in level_permissions:
            # -1 is for @everyone
            if -1 in level_permissions[level.name] or any(
                str(check.id) in level_permissions[level.name] for check in checkables
            ):
                return True

    return False

class ClaimThread(commands.Cog):
    """Allows supporters to claim thread by sending claim in the thread channel"""
    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.plugin_db.get_partition(self)

        check_reply.fail_msg = 'This thread has been claimed by another user.'

        self.bot.get_command('reply').add_check(check_reply)
        self.bot.get_command('areply').add_check(check_reply)
        self.bot.get_command('fareply').add_check(check_reply)
        self.bot.get_command('freply').add_check(check_reply)

    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @checks.thread_only()
    @commands.command()
    async def claim(self, ctx):
        """Claims the thread"""

        thread = await self.db.find_one({'thread_id': str(ctx.thread.channel.id)})

        if thread is None:
            await self.db.insert_one({'thread_id': str(ctx.thread.channel.id), 'claimers': [str(ctx.author.id)]})
            await ctx.send('Claimed')
        else:
            await ctx.send('Thread is already claimed')

    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @checks.thread_only()
    @commands.command(aliases=["uclaim"])
    async def unclaim(self, ctx):
        """Unclaims the thread"""

        thread = await self.db.find_one({'thread_id': str(ctx.thread.channel.id)})

        if thread is None:
            await ctx.send('Thread is not claimed')
        elif str(ctx.author.id) in thread['claimers'] or await check_user_level_permissions(ctx):
            await self.db.delete_one({'thread_id': str(ctx.thread.channel.id)})
            await ctx.send('Unclaimed')

        cat = ctx.channel.category

        if self.bot.cogs['CategoryNotifier'] and cat and str(cat.id) in self.bot.cogs['CategoryNotifier'].config['mappings']:
            role_id = int(self.bot.cogs['CategoryNotifier'].config['mappings'][str(cat.id)])
            role = ctx.guild.get_role(role_id)
            if role:
                await ctx.send(content=role.mention)

    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @checks.thread_only()
    @commands.command(aliases=["aclaim"], usage="[member]")
    async def addclaim(self, ctx, *, member: discord.Member):
        """Adds another user to the thread claimers"""

        thread = await self.db.find_one({'thread_id': str(ctx.thread.channel.id)})

        if thread and (str(ctx.author.id) in thread['claimers'] or await check_user_level_permissions(ctx)):
            await self.db.find_one_and_update({'thread_id': str(ctx.thread.channel.id)}, {'$addToSet': {'claimers': str(member.id)}})
            await ctx.send('Added to claimers')

    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @checks.thread_only()
    @commands.command(aliases=["rclaim"], usage="[member]")
    async def removeclaim(self, ctx, *, member: discord.Member):
        """Removes a user from the thread claimers"""

        thread = await self.db.find_one({'thread_id': str(ctx.thread.channel.id)})

        if thread and (str(ctx.author.id) in thread['claimers'] or await check_user_level_permissions(ctx)):
            await self.db.find_one_and_update({'thread_id': str(ctx.thread.channel.id)}, {'$pull': {'claimers': str(member.id)}})
            await ctx.send('Removed from claimers')

    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @checks.thread_only()
    @commands.command(aliases=["tclaim"], usage="[member]")
    async def transferclaim(self, ctx, *, member: discord.Member):
        """Removes all users from claimers and gives another member all control over thread"""

        thread = await self.db.find_one({'thread_id': str(ctx.thread.channel.id)})

        if thread and (str(ctx.author.id) in thread['claimers'] or await check_user_level_permissions(ctx)):
            await self.db.find_one_and_update({'thread_id': str(ctx.thread.channel.id)}, {'$set': {'claimers': [str(member.id)]}})
            await ctx.send('Added to claimers')

async def check_reply(ctx):
    thread = await ctx.bot.get_cog('ClaimThread').db.find_one({'thread_id': str(ctx.thread.channel.id)})

    if thread:
        return ctx.author.bot or str(ctx.author.id) in thread['claimers'] or await check_user_level_permissions(ctx)

    return True

async def setup(bot):
    await bot.add_cog(ClaimThread(bot))