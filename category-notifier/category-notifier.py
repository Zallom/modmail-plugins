import discord
from discord.ext import commands
from core.models import PermissionLevel
from core import checks

class CategoryNotifier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.plugin_db.get_partition(self)
        self.config = {
            "enabled": True,
            "mappings": {}  # category_id -> role_id
        }

    async def cog_load(self):
        db_config = await self.db.find_one({"_id": "category_notifier"})
        if db_config is None:
            await self.db.find_one_and_update(
                {"_id": "category_notifier"},
                {"$set": self.config},
                upsert=True
            )
        else:
            self.config.update(db_config)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        if not self.config["enabled"]:
            return

        cat = after.category
        if cat and str(cat.id) in self.config["mappings"]:
            role_id = int(self.config["mappings"][str(cat.id)])
            role = after.guild.get_role(role_id)
            if role:
                await after.send(content=role.mention)

    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    @commands.group(name="notifier", invoke_without_command=True)
    async def notifier(self, ctx):
        """Configure the category notifier"""
        await ctx.send_help(ctx.command)

    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    @notifier.command(name="toggle")
    async def notifier_toggle(self, ctx):
        """Enable or disable the notifier"""
        self.config["enabled"] = not self.config["enabled"]
        await self._commit()
        await ctx.send(f"Category Notifier is now {'enabled' if self.config['enabled'] else 'disabled'}.")

    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    @notifier.command(name="add")
    async def notifier_add(self, ctx, category: discord.CategoryChannel, role: discord.Role):
        """Link a category to a role"""
        self.config["mappings"][str(category.id)] = str(role.id)
        await self._commit()
        await ctx.send(f"Linked category `{category.name}` to role `{role.name}`.")

    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    @notifier.command(name="remove")
    async def notifier_remove(self, ctx, category: discord.CategoryChannel):
        """Remove a category link"""
        if str(category.id) in self.config["mappings"]:
            del self.config["mappings"][str(category.id)]
            await self._commit()
            await ctx.send(f"Removed category `{category.name}` from notifier.")
        else:
            await ctx.send("This category isn't linked.")

    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    @notifier.command(name="list")
    async def notifier_list(self, ctx):
        """List all category->role mappings"""
        if not self.config["mappings"]:
            return await ctx.send("No mappings set.")
        lines = []
        for cat_id, role_id in self.config["mappings"].items():
            cat = ctx.guild.get_channel(int(cat_id))
            role = ctx.guild.get_role(int(role_id))
            if cat and role:
                lines.append(f"{cat.name} → {role.mention}")
        await ctx.send("\n".join(lines))

    async def _commit(self):
        await self.db.find_one_and_update(
            {"_id": "category_notifier"},
            {"$set": self.config},
            upsert=True
        )

async def setup(bot):
    await bot.add_cog(CategoryNotifier(bot))