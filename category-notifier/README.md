# Category Notifier

Automatically mention a role when a modmail thread is moved to a specific category. Perfect for notifying specialized support teams when threads need their attention.

## Installation

This plugin works on the modmail bot made by kyb3r. You can find the bot [here](https://github.com/modmail-dev/modmail). Use the command below to install this plugin into your bot.

`[p]plugins add zallom/modmail-plugins/category-notifier`

## Usage

The plugin features a set of commands to configure automatic role mentions when threads are moved to specific categories.
All commands start with `[p]notifier` and is omitted from the command list below.

> ### Main commands

`toggle`
Enable or disable the category notifier.

`add (category) (role)`
Link a category to a role. When a thread is moved to this category, the role will be mentioned.

`remove (category)`
Remove a category link.

`list`
List all category->role mappings currently configured.

## How it works

When a modmail thread channel is moved to a category that has a linked role, the bot will automatically send a message mentioning that role in the thread. This allows you to notify specific support teams (e.g., billing, technical support, etc.) when a thread needs their attention.

## Credits

This plugin was created by Zallom ([github.com/Zallom](https://github.com/Zallom) or @zallom) and is licensed under the MIT license. Whilst not required, it would be appreciated if you could credit me if you use this plugin or its code anywhere.
