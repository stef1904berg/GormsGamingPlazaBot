import discord
from discord import app_commands
import os
from dotenv import load_dotenv
from Whitelist import Whitelist
from PterodactylApi import PterodactylApi, parse_servers

load_dotenv()
MY_GUILD = discord.Object(id=os.getenv('GUILD_ID'))

PTERO_SERVERS = os.getenv('PTERO_SERVERS')
PTERO_DOMAIN = os.getenv('PTERO_DOMAIN')
BEARER_TOKEN = os.getenv("PTERO_TOKEN")
SERVERS = parse_servers(PTERO_SERVERS)


class GormClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.whitelist = Whitelist()
        self.ptero_api = PterodactylApi(BEARER_TOKEN, PTERO_DOMAIN, SERVERS)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
