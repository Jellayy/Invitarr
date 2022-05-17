Inspired by: [Sleepingpirates/Invitarr](https://github.com/Sleepingpirates/Invitarr)
<br>
Invitarr is a discord bot that automates and manages inviting users in a Discord server to a Plex server.
## Features
Invitarr can:
 - Use the Plex API to connect to multiple Plex accounts and servers at once
 - Monitor a role in a Discord server to serve Plex invites to users who get the role
 - Load balance Plex server invites upon connected servers
 - Store users' invite information in a local database
 - More coming soon!
## Installation & Usage
1. Create a bot on the [Discord Applications page](https://discord.com/developers/applications)
2. Make sure your bot has access to the `GUILD_MEMBERS` intent
3. Deploy the bot using one of the methods below:
### Docker Compose
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
    restart: no
```
### Docker CLI
```
docker run -d \
  --name=invitarr \
  -e TZ=America/Phoenix \
  -v /path/to/data:/config \
  --restart no \
  jellayy/invitarr:latest
```
Note: It is recommended to set 'restart' to 'no' until you have populated your config.ini file. After finishing the setup process, feel free to change 'restart' to 'unless-stopped'
4. Run the bot once to generate an empty config.ini file in the /config directory
5. Configure the `config.ini` file
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
```
See the example below for adding multiple Plex accounts or servers to the config:
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
```
Assuming you have configured everything correctly, Invitarr will send DM invites to any user that receives the configured monitored role. Make sure your users have their DMs open!
## Commands
`.get_db` Sends a txt copy of the user DB to discord. This contains users' Plex emails. If your users don't want these publicly shared, restrict the bot's access to public channels.
