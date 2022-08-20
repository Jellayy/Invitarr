![GitHub Workflow Status](https://img.shields.io/github/workflow/status/jellayy/invitarr/Build%20Docker%20images?style=for-the-badge)
![GitHub repo size](https://img.shields.io/github/repo-size/jellayy/invitarr?style=for-the-badge)
![Docker Pulls](https://img.shields.io/docker/pulls/jellayy/invitarr?style=for-the-badge)

Inspired by: [Sleepingpirates/Invitarr](https://github.com/Sleepingpirates/Invitarr)
<br>
Invitarr is a discord bot that automates and manages inviting users in a Discord server to a Plex server.

## Sections
- [Features](#features)
- [Installation](#installation)
  - [Register your Discord Bot](#register-your-discord-bot)
  - [Deploy to Docker](#deploy-to-docker)
  - [Updating to v2.0](#updating-to-v20)
- [Usage](#usage)
  - [Commands](#commands)

## Features
Invitarr can:
 - Use the Plex API to connect to multiple Plex accounts and servers at once
 - Monitor a role in a Discord server to serve Plex invites to users who get the role
 - Load balance Plex server invites upon connected servers
 - Create Overseerr accounts for invited users to send requests
 - Store users' Plex and Overseerr information in a local database for state management
 - More coming soon!
## Installation
### Register your Discord bot
1. Create a bot on the [Discord Applications page](https://discord.com/developers/applications)
2. Make sure your bot has access to the `GUILD_MEMBERS` intent
### Deploy to Docker
#### Docker Compose
```
---
version: "2.1"
services:
  invitarr:
    image: jellayy/invitarr:latest
    container_name: invitarr
    environment:
      - TZ=America/Phoenix
    volumes:
      - /path/to/data:/config
```
#### Docker CLI
```
docker run -d \
  --name=invitarr \
  -e TZ=America/Phoenix \
  -v /path/to/data:/config \
  jellayy/invitarr:latest
```
Note: It is recommended to omit any restart policy until you have populated your config.ini file. After finishing the setup process, feel free to change 'restart' to 'unless-stopped'
### Configure
1. Run the bot once to generate an empty config.ini file in the /config directory
2. Configure the `config.ini` file:
```
[Discord]
command prefix = .
bot token = YOUR_BOT_TOKEN

[Plex Accounts]
num accounts = 1

[Plex Account 0]
user = YOUR_EMAIL_OR_USER
password = YOUR_PASSWORD
num servers = 1
server 0 = YOUR_SERVER_NAME

[Role Monitoring]
enable = 1
monitored role = YOUR_DISCORD_ROLE_NAME

[Overseer Account Management]
enable = 0
```
See the example below for all config options and configuration of multiple plex accounts and servers:
```
[Discord]
command prefix = .
bot token = YOUR_BOT_TOKEN

[Plex Accounts]
num accounts = 2

[Plex Account 0]
user = YOUR_EMAIL_OR_USER
password = YOUR_PASSWORD
num servers = 2
server 0 = YOUR_SERVER_NAME_1
server 1 = YOUR_SERVER_NAME_2

[Plex Account 1]
user = YOUR_EMAIL_OR_USER
password = YOUR_PASSWORD
num servers = 1
server 0 = YOUR_SERVER_NAME

[Role Monitoring]
enable = 1
monitored role = YOUR_DISCORD_ROLE_NAME

[Overseer Account Management]
enable = 1

[Overseerr Settings]
overseerr server = http://YOUR.OVERSEERR.ADDRESS
api key = YOUR_OVERSEERR_KEY
```
Assuming you have configured everything correctly, Invitarr will send DM invites to any user that receives the configured monitored role. Make sure your users have their DMs open!
### Updating to v2.0
Invitarr v2.0 uses an updated database structure that stores more information to allow for easier implementation of features going into the future. If Invitarr v2.0 detects a v1.x database, it will recreate it as a 2.0 database. This process has proven to be pretty stable; however, it is still recommended to backup your v1.x database before updating to v2.0 in the event that anything goes wrong during the update. Your database file can be found at `/config/invitarr.db`

## Usage

### Commands
`.get_db` (Administrator needed) Sends a txt copy of the user DB to discord. This contains a lot of identifying information about both your users and your own plex account. If you don't want these publicly shared, restrict the bot's access to public channels.

`.add_user @USER EMAIL (OPT)CREATE_OVERSEERR_ACCOUNT[True/False]` (Administrator needed) Admin command for manually sharing, creating an overseerr account, and adding a user to the database. Bypasses standard rolemonitoring limitation of one invite and overseerr account per discord user. Error handling currently not the most fleshed out, feel free to create issues as unhandled cases arise.

`.delete_user EMAIL` (Administrator needed) Removes a given user from plex shares and deletes their associated Overseerr account if available.

`.force_delete_user EMAIL` (Administrator needed) Sometimes, due to users not accepting plex invites or API failures, the database can become out of sync to the point where `.delete_user` can no longer safely remove users. Use this to bypass all checks and attempt to forcibly purge a user from Plex, Overseerr, and the database. No matter the status of the user in Plex/Overseerr, this command will remove that user from the database and must have the monitored role reinstated to be managed by Invitarr. Naturally very destructive so only use when `.delete_user` cannot be used.
