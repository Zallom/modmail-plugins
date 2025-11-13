# Claim Thread

Allows supporters to claim modmail threads, ensuring only the claimers can reply to the thread. This prevents multiple staff members from responding to the same user simultaneously.

## Installation

This plugin works on the modmail bot made by kyb3r. You can find the bot [here](https://github.com/modmail-dev/modmail). Use the command below to install this plugin into your bot.

`[p]plugins add zallom/modmail-plugins/claim`

## Usage

The plugin features a set of commands to manage thread claims.
All commands require the Supporter permission level or higher and can only be used in thread channels.

> ### Main commands

`claim`
Claims the current thread. Once claimed, only the claimer(s) can use reply commands (reply, areply, freply, fareply).

`unclaim` (alias: `uclaim`)
Unclaims the current thread, allowing anyone to reply again. Can be used by the original claimer or by moderators/administrators. If the CategoryNotifier plugin is enabled, it will mention the configured role for the category.

`addclaim (member)` (alias: `aclaim`)
Adds another user to the thread claimers. Only the current claimer(s) or moderators/administrators can add claimers.

`removeclaim (member)` (alias: `rclaim`)
Removes a user from the thread claimers. Only the current claimer(s) or moderators/administrators can remove claimers.

`transferclaim (member)` (alias: `tclaim`)
Transfers the claim to another member, removing all current claimers and giving full control to the specified member.

## How it works

When a thread is claimed, the plugin adds a check to the reply commands (reply, areply, freply, fareply) that prevents non-claimers from using them. Only the user(s) who claimed the thread or users with moderator+ permissions can reply to claimed threads.

This is useful for:
- Preventing multiple staff members from responding to the same user
- Ensuring continuity in support conversations
- Allowing staff to "take ownership" of specific support cases

## Integration with Category Notifier

This plugin has built-in integration with the [Category Notifier plugin](https://github.com/Zallom/modmail-plugins/tree/main/category-notifier). When a thread is unclaimed, if a role is configured for the thread's category, that role will be automatically mentioned.

## Credits

This plugin was created by fourjr ([github.com/fourjr](https://github.com/fourjr/) or @fourjr) and modified by Zallom ([github.com/Zallom](https://github.com/Zallom) or @zallom) and is licensed under the MIT license. Whilst not required, it would be appreciated if you could credit us if you use this plugin or its code anywhere.
