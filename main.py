import os
from typing import Literal

from dotenv import load_dotenv
import discord
from GormClient import GormClient
from PterodactylApi import parse_servers, PterodactylApi

load_dotenv()

intents = discord.Intents.default()
intents.messages = True
intents.members = True

client = GormClient(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print(f"Pterodactyl url: {client.ptero_api.api_url}")
    print(f"Servers: {client.ptero_api.servers}")
    print("------")


whitelist_options = Literal[
    "add",
    "remove",
    "list"
]


@client.tree.command()
async def whitelist(interaction: discord.Interaction, action: whitelist_options, player_name: str):
    if action == "add":
        if client.whitelist.is_whitelisted(player_name):
            await interaction.response.send_message(f"`{player_name}` is already on the whitelist!", ephemeral=True)
            return

        result = client.whitelist.add(player_name)
        if result:
            await interaction.response.send_message(f"`{player_name}` has been added to the whitelist!", ephemeral=True)
            client.ptero_api.upload_whitelist(client.whitelist.whitelist)

        else:
            await interaction.response.send_message(f"`{player_name}` couldn't be added to the whitelist.", ephemeral=True)

    if action == "remove":
        if not client.whitelist.is_whitelisted(player_name):
            await interaction.response.send_message(f"`{player_name}` is already removed from the whitelist!", ephemeral=True)
            return

        result = client.whitelist.remove(player_name)
        if result:
            await interaction.response.send_message(f"`{player_name}` has been removed to the whitelist!", ephemeral=True)
            client.ptero_api.upload_whitelist(client.whitelist.whitelist)

        else:
            await interaction.response.send_message(f"`{player_name}` couldn't be removed from the whitelist!", ephemeral=True)
    if action == "list":
        whitelist_out = ""
        for whitelisted_player in client.whitelist.whitelist:
            whitelist_out += f"`{whitelisted_player['name']}`\n"
        await interaction.response.send_message(whitelist_out, ephemeral=True)


client.run(os.getenv("BOT_TOKEN"))
