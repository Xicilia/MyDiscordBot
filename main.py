import discord
import asyncio
from discord.ext import commands, tasks

################# COGS ###########################
from cogs.templateCog import TemplateCog
from cogs.sheetsCog import SheetCog
from cogs.gallowCog import GallowCog
from cogs.httpCog import HttpCog
from cogs.nicknamesCog import NicknamesCog
from cogs.wildberriesCog import WildberriesCog
from cogs.roleplayCog import RPCog
from cogs.horoCog import HoroCog
##################################################

from misc.globals import settings
from misc.schedulers import ScheduleTasksManager
from misc.bot import Bot
from misc.logs import simpleLog, errorLog

async def initCogs(bot: commands.Bot, cogs):
    """
    adds cogs to bot.
    """
    simpleLog("COGS", "Started initializing cogs.")
    for cog in cogs:
        
        await bot.add_cog(cog(bot))
        simpleLog("COGS", f"Initialized cog \"{cog.__name__}\"")


intents = discord.Intents.default()
intents.message_content = True

bot = Bot(settings.getSetting("commandPrefix"), intents)
scheduler = ScheduleTasksManager(bot)

#all cogs list
cogs = [TemplateCog, SheetCog, HttpCog, NicknamesCog, WildberriesCog, GallowCog, RPCog, HoroCog]

asyncio.run(initCogs(bot, cogs))
    
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Аватария"))
    
    scheduler.start()
    
    
@bot.event
async def on_command_error(ctx: commands.Context, error):
    
    if isinstance(error, commands.CommandNotFound):
        
        embed = discord.Embed()
        embed.set_image(url="https://media.tenor.com/PTV9EiisgY8AAAAC/walterwhite.gif")
        await ctx.reply("Такой команды нет :nerd:", embed=embed)
        
bot.run(settings.getSetting("botToken"))