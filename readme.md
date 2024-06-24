# DiscordCalendar

This upon running starts a Discord bot, type the basic commands for Google Calendar Events in the bot and the Bot will complete the tasks.

## Setup Instructions

### 1. Set up Environment Variables

Create a `.env` file in the root directory of your project and add the following variables:

```dotenv
# .env file
GOOGLE_API_KEY="api_key_here"
DISCORD_BOT_TOKEN="api_key_here"
```
### 2. Configure Credentials

Create a credentials.json file in the same directory. This file can be downloaded from the Google Calendar API OAuth 2.0 Credentials page after setting up your credentials.

### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install python-dotenv
```
### 4. Composio Integration

  #### 4.1 Install Composio

  Install the Composio CLI package:
  ```bash
pip install composio_crewai
```
  #### 4.2 Add GitHub Repository

  Add your GitHub repository to Composio:
  ```bash
composio add github
```
  #### 4.3 Install Apps

  Install necessary apps or tools using Composio:
  ```bash
composio apps
```
## Contribution

You can add more Commands to the bot.
Please work on a different branch until it is approved or send me a message.

