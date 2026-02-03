import discord
from Message import Message
from discord.ext import commands
from discord import app_commands 
ID = 908732286978113568
GUILD_ID = discord.Object(id=ID)

class Bot(commands.Bot):
    def __init__(self,command_prefix,intents):

        super().__init__(command_prefix=command_prefix,intents=intents)
        self.vc:discord.VoiceClient | None = None
        self.current_music = None
        self.message = Message() 
        self.isGoto = False 

    async def on_ready(self):
        print(self.message.welcome)

        try:
            
            guild = discord.Object(id=ID)
            synced = await self.tree.sync(guild=guild) 
            print(f"Syncronysation {len(synced)} to {guild.id}")

        except Exception as e:

            print(e)


    async def on_message(self,message):
        if message.author == self.user:
            return


