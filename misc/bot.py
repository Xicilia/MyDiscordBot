import discord
from discord.ext import commands
from discord.message import Message

from misc.globals import guildId
from misc.logs import simpleLog

from random import choice

#add some fun to answers
_emojiList = [
    ":cowboy:",
    ":face_holding_back_tears:",
    ":nerd:",
    ":sunglasses:",
    ":disguised_face:",
    ":rage:",
    ":sneezing_face:",
    ":mask:",
    ":japanese_ogre:",
    ":smiley_cat:",
    ":smirk_cat:",
    ":scream_cat:",
    ":pouting_cat:",
    ":heart_eyes_cat:",
    ":crying_cat_face:",
    ":thumbsup:",
    ":love_you_gesture:",
    ":ok_hand:",
    ":pray:",
    ":v:",
    ":cat:",
    ":mouse:",
    ":cat2:",
    ":black_cat:"
]

class Bot(commands.Bot):
    """
    Basic commands.Bot with implemented setup hook and on_message event
    """
    def __init__(self, command_prefix: str, intents: discord.Intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        
    async def setup_hook(self):

        await self.tree.sync(guild=discord.Object(id=guildId))  
        simpleLog("BOT", f"Synced commands. Guild: {guildId}")
        
    async def on_message(self, message: Message):
        
        if message.content.lower() == "спасибо кот" or message.content.lower() == "спасибо, кот":
            
            simpleLog("BOT", f"User {message.author.name} (ID: {message.author.id}) thanked cat :)")
            await message.channel.send(f"Пожалуйста <@{message.author.id}> {choice(_emojiList)}")
            return
        
        await self.process_commands(message)
        
        
        
    