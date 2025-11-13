# Advanced Menu - JSON Configuration Documentation

This document provides a complete reference for the JSON configuration format used by the Advanced Menu plugin.

## Table of Contents
- [Root Configuration](#root-configuration)
- [Options](#options)
- [Submenus](#submenus)
- [Modals](#modals)
- [Complete Example](#complete-example)

## Root Configuration

The root level of the configuration contains global settings for the menu system.

```json
{
  "_id": "advanced-menu",
  "enabled": true,
  "anonymous_menu": false,
  "close_on_timeout": false,
  "close_on_timeout_message": "The menu selection timed out.",
  "timeout": 200,
  "embed_text": "Please select an issue type.",
  "dropdown_placeholder": "What is your issue?",
  "auto_move_contact_threads": true,
  "contact_category_id": "ID",
  "reopen_modal_button_emoji": "📝",
  "reopen_modal_button_label": "Reopen modal",
  "options": {},
  "submenus": {},
  "modals": {}
}
```

### Root Configuration Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `_id` | string | Yes | - | Database identifier, must be `"advanced-menu"` |
| `enabled` | boolean | Yes | `false` | Whether the menu is active |
| `anonymous_menu` | boolean | No | `false` | If `true`, menu messages are sent anonymously (without staff member name) |
| `close_on_timeout` | boolean | No | `false` | If `true`, closes the thread when the menu times out |
| `close_on_timeout_message` | string | No | `"The menu selection timed out."` | Message shown when closing due to timeout |
| `timeout` | number | Yes | `20` | Time in seconds before the menu times out (minimum 1) |
| `embed_text` | string | Yes | `"Please select an option."` | Main text displayed above the dropdown menu |
| `dropdown_placeholder` | string | Yes | `"Select an option to contact the staff team."` | Placeholder text shown in the dropdown before selection |
| `auto_move_contact_threads` | boolean | No | `false` | If `true`, automatically moves threads created with the contact command to the specified category |
| `contact_category_id` | string | No | `null` | Discord category ID to move contact threads to (only used if `auto_move_contact_threads` is `true`) |
| `reopen_modal_button_emoji` | string | No | `"📝"` | Emoji displayed on the button to reopen a modal |
| `reopen_modal_button_label` | string | No | `"Reopen modal"` | Label text for the button to reopen a modal |
| `options` | object | Yes | `{}` | Main menu options (see [Options](#options)) |
| `submenus` | object | No | `{}` | Submenu definitions (see [Submenus](#submenus)) |
| `modals` | object | No | `{}` | Modal form definitions (see [Modals](#modals)) |

## Options

Options are the selectable items shown in dropdown menus. They can execute commands, open modals, or navigate to submenus.

### Option Structure

Each option is stored as a key-value pair where:
- **Key**: Sanitized version of the label (lowercase, spaces replaced with underscores)
- **Value**: Option configuration object

```json
"options": {
  "appeal": {
    "label": "Appeal",
    "description": "Appeal a sanction",
    "emoji": "🛠️",
    "type": "modal",
    "callback": "appeal"
  },
  "technical_support": {
    "label": "Technical Support",
    "description": "Get help with technical issues",
    "emoji": "💻",
    "type": "submenu",
    "callback": "tech_submenu"
  },
  "close_request": {
    "label": "Close Request",
    "description": "Close this thread",
    "emoji": "🔒",
    "type": "command",
    "callback": "close Thread closed by user request"
  }
}
```

### Option Fields

| Field | Type | Required | Max Length | Description |
|-------|------|----------|------------|-------------|
| `label` | string | Yes | 100 | Display name shown in the dropdown |
| `description` | string | Yes | 100 | Brief description shown under the label |
| `emoji` | string | Yes | - | Emoji displayed next to the option |
| `type` | string | Yes | - | Type of action: `"command"`, `"submenu"`, or `"modal"` |
| `callback` | string | Yes | - | Reference to what to execute (depends on type) |

### Option Types

#### 1. Command Type
Executes a modmail bot command when selected.

```json
{
  "type": "command",
  "callback": "move 123456789"
}
```

- The `callback` is the command to execute (without the prefix)
- Can include command arguments
- Examples: `"close Resolved"`, `"move 123456789"`, `"reply Thanks for contacting us!"`

#### 2. Submenu Type
Opens another dropdown menu with additional options.

```json
{
  "type": "submenu",
  "callback": "billing_options"
}
```

- The `callback` is the key of a submenu defined in the `submenus` object
- Must reference an existing submenu
- Maximum 25 options in main menu, 24 in submenus (Discord limitation)

#### 3. Modal Type
Opens a form dialog for the user to fill out.

```json
{
  "type": "modal",
  "callback": "appeal"
}
```

- The `callback` is the key of a modal defined in the `modals` object
- Must reference an existing modal
- After submission, shows a "Reopen modal" button

## Submenus

Submenus are secondary dropdown menus that can be accessed from main menu options or other submenus.

### Submenu Structure

```json
"submenus": {
  "tech_submenu": {
    "bot_issue": {
      "label": "Bot Issue",
      "description": "Report a bot malfunction",
      "emoji": "🤖",
      "type": "modal",
      "callback": "bot_report"
    },
    "account_issue": {
      "label": "Account Issue",
      "description": "Problems with your account",
      "emoji": "👤",
      "type": "command",
      "callback": "move 987654321"
    }
  }
}
```

### Submenu Features

- Each submenu is a collection of options with the same structure as main menu options
- Automatically includes a "Main menu" option (🏠) to return to the main menu
- Can contain up to 24 options (Discord limitation - 1 slot reserved for "Main menu")
- Can reference other submenus for nested navigation
- Cannot use "Main menu" or "main_menu" as an option label

## Modals

Modals are form dialogs that collect user input through text fields.

### Modal Structure

```json
"modals": {
  "appeal": {
    "title": "Appeal",
    "anonymous": false,
    "fields": [
      {
        "label": "What is your sanction?",
        "placeholder": "e.g., Ban, Mute, Warn",
        "style": 1
      },
      {
        "label": "Explain your appeal",
        "placeholder": "Provide details about your appeal",
        "style": 2
      }
    ],
    "response_embed": {
      "description": "Thanks {recipient.mention} for appealing!",
      "color": "0x00ff00",
      "footer": {
        "text": "Appeal Team",
        "icon_url": "https://example.com/icon.png"
      },
      "thumbnail_url": "https://example.com/thumbnail.png",
      "image_url": "https://example.com/image.png",
      "show_timestamp": true
    },
    "type": "command",
    "callback": "move 123456789"
  }
}
```

### Modal Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | Title displayed at the top of the modal dialog |
| `anonymous` | boolean | No | If `true`, sends responses anonymously (default: `false`) |
| `fields` | array | Yes | Array of input fields (max 5 due to Discord limitation) |
| `response_embed` | object | No | Custom embed shown after form submission |
| `type` | string | No | If `"command"`, executes callback after submission |
| `callback` | string | No | Command to run after submission (only if `type` is `"command"`) |

### Field Object

Each field in the `fields` array:

```json
{
  "label": "Field label",
  "placeholder": "Placeholder text (optional)",
  "style": 1
}
```

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `label` | string | Yes | Label displayed above the input field |
| `placeholder` | string | No | Placeholder text shown in empty field |
| `style` | number | Yes | Input style: `1` = short (single line), `2` = long (paragraph) |

### Response Embed Object

The `response_embed` customizes the confirmation message:

```json
{
  "description": "Thanks {recipient.mention} for your submission!",
  "color": "0x00ff00",
  "footer": {
    "text": "Footer text",
    "icon_url": "https://example.com/icon.png"
  },
  "thumbnail_url": "https://example.com/thumbnail.png",
  "image_url": "https://example.com/image.png",
  "show_timestamp": true
}
```

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `description` | string | No | Main text of the embed. Supports `{recipient.mention}` placeholder |
| `color` | string/number | No | Embed color as hex string (e.g., `"0x00ff00"`) or number |
| `footer` | object | No | Footer configuration with `text` and optional `icon_url` |
| `thumbnail_url` | string | No | URL for small image in top right corner |
| `image_url` | string | No | URL for large image at bottom |
| `show_timestamp` | boolean | No | If `true`, shows current timestamp in footer |

### Modal Behavior

1. When a modal option is selected, the form dialog opens
2. User fills out the fields (required by Discord)
3. Upon submission:
   - Custom embed (if configured) is sent to the user and thread
   - User's responses are sent in a separate embed with all field answers
   - If `type` is `"command"`, the specified command is executed
   - A "Reopen modal" button appears, allowing the user to submit again

## Complete Example

```json
{
  "_id": "advanced-menu",
  "enabled": true,
  "anonymous_menu": false,
  "close_on_timeout": false,
  "close_on_timeout_message": "The menu selection timed out.",
  "timeout": 300,
  "embed_text": "Welcome! Please select a support category.",
  "dropdown_placeholder": "Choose your issue type",
  "auto_move_contact_threads": true,
  "contact_category_id": "123456789012345678",
  "reopen_modal_button_emoji": "📝",
  "reopen_modal_button_label": "Submit another form",
  "options": {
    "appeal": {
      "label": "Appeal",
      "description": "Appeal a ban or sanction",
      "emoji": "⚖️",
      "type": "modal",
      "callback": "appeal_form"
    },
    "support": {
      "label": "Technical Support",
      "description": "Get technical assistance",
      "emoji": "💻",
      "type": "submenu",
      "callback": "support_menu"
    },
    "general": {
      "label": "General Question",
      "description": "Ask a general question",
      "emoji": "❓",
      "type": "command",
      "callback": "move 987654321098765432"
    }
  },
  "submenus": {
    "support_menu": {
      "bot_issue": {
        "label": "Bot Not Working",
        "description": "Report bot malfunction",
        "emoji": "🤖",
        "type": "modal",
        "callback": "bug_report"
      },
      "account_help": {
        "label": "Account Help",
        "description": "Issues with your account",
        "emoji": "👤",
        "type": "command",
        "callback": "move 111222333444555666"
      }
    }
  },
  "modals": {
    "appeal_form": {
      "title": "Ban Appeal Form",
      "anonymous": false,
      "fields": [
        {
          "label": "Your Discord Username",
          "placeholder": "Username#0000",
          "style": 1
        },
        {
          "label": "Sanction Type",
          "placeholder": "Ban, Mute, Kick, etc.",
          "style": 1
        },
        {
          "label": "Reason for Appeal",
          "placeholder": "Explain why you believe the sanction should be removed",
          "style": 2
        }
      ],
      "response_embed": {
        "description": "Thank you {recipient.mention} for submitting your appeal!\n\nOur team will review it shortly.",
        "color": "0x3498db",
        "footer": {
          "text": "Appeals Team"
        },
        "show_timestamp": true
      },
      "type": "command",
      "callback": "move 123456789012345678"
    },
    "bug_report": {
      "title": "Bug Report",
      "fields": [
        {
          "label": "What went wrong?",
          "placeholder": "Brief description",
          "style": 1
        },
        {
          "label": "Steps to reproduce",
          "placeholder": "Detailed steps",
          "style": 2
        }
      ],
      "response_embed": {
        "description": "Thanks for the bug report!",
        "color": "0xe74c3c"
      },
      "type": "command",
      "callback": "move 999888777666555444"
    }
  }
}
```

## Tips and Best Practices

### Limitations
- **Main menu**: Maximum 25 options (Discord limitation)
- **Submenus**: Maximum 24 options (1 slot reserved for "Main menu" button)
- **Modal fields**: Maximum 5 fields per modal (Discord limitation)
- **Description length**: Maximum 100 characters per option description
- **Label uniqueness**: Each option label within a menu must be unique

### Recommendations
1. **Use submenus** for complex category structures instead of cramming everything in the main menu
2. **Keep descriptions short** and clear (under 100 characters)
3. **Use appropriate emojis** to make options visually distinct
4. **Set reasonable timeouts** (2-5 minutes is typical)
5. **Test your modals** - ensure forms are clear and fields make sense
6. **Use commands wisely** - the `callback` for command types can chain multiple commands
7. **Consider anonymous mode** for sensitive topics where staff identity shouldn't be revealed

### Common Patterns

#### Multi-level Support System
```
Main Menu
├─ Appeals (modal)
├─ Technical Support (submenu)
│  ├─ Bot Issues (modal)
│  ├─ Account Issues (command)
│  └─ Other (submenu)
└─ General Questions (command)
```

#### Category-based Routing
Use command type with `move <category_id>` to automatically route threads to appropriate channels:
```json
{
  "type": "command",
  "callback": "move 123456789"
}
```

#### Form then Action
Use modals with `type: "command"` to collect information and then automatically move or process:
```json
{
  "type": "command",
  "callback": "move 123456789"
}
```
This executes after the user submits the modal.

## Formatting Support

### In Embed Descriptions
You can use Discord markdown and the following placeholders:
- `{recipient.mention}` - Mentions the user
- Standard Discord formatting (bold, italic, code blocks, etc.)

### In Commands
The `callback` for command types supports:
- Any valid modmail bot command
- Command arguments
- Multiple commands cannot be chained in a single callback