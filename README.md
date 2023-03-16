# Gorms Gaming Plaza Bot
A simple discord bot for managing a single whitelist across multiple servers hosted on [Pterodactyl](https://pterodactyl.io/).
The bot allows you to sync one whitelist between all chosen servers.

Enviroment variables:
- `BOT_TOKEN`: The token the discord bot runs on
- `GUILD_ID`: The guild id of the discord server the bot runs in
- `PTERO_SERVERS`: A list of pterodactyl server identifiers seperated by a `,` 
- `PTERO_DOMAIN`: The url the pterodactyl instance listens on
- `PTERO_TOKEN`: API key for accessing the Pterodactyl api