import discord
from discord.ext import commands
from cogs.cog import Cog

from misc.globals import guildId
from misc.logs import simpleLog, errorLog
from misc.httpManager import *

class HttpCog(Cog):
    """
    Cog that contains all commands which gets information through http requests.
    """
    
    randStuffContentStartString = "<table class=\"text\"><tr><td>"
    randStuffContentEndFact = "</td>"
    randStuffContentEndWisdom = "<span class=\"author\">"
    
    _factsUrl = "https://randstuff.ru/fact/"
    _wisdomUrl = "https://randstuff.ru/saying/"
    _castlotsUrl = "http://castlots.org/generator-anekdotov-online/generate.php"
    
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)
        
    @commands.hybrid_command(name="факт", description="Случайный факт", with_app_command=True)
    @discord.app_commands.guilds(discord.Object(id = guildId))
    async def getFact(self, ctx: commands.Context):
        """
        Gets random fact from randstuff.ru
        """
        
        await ctx.defer()
        
        #all page text
        content = HttpRequestManager.getRequest(HttpCog._factsUrl)
        
        simpleLog("HTTP", f"User {ctx.author.name} (ID: {ctx.author.id}) getting random fact.")
        
        if content.statusCode != 200:
            #something wrong with host
            
            errorLog("HTTP", "Can't get random fact. REASON: response code from api is not 200")
            await ctx.reply("Чето не так с сайтиком")
            return
        
        #find content div start
        contentStart = content.answer.find(HttpCog.randStuffContentStartString)
        #find content div end based on content start
        contentEnd = content.answer.find(HttpCog.randStuffContentEndFact, contentStart)
        
        #fact is page text slice where content start is slice start and content end is slice end
        await ctx.reply( content.answer[contentStart + len(HttpCog.randStuffContentStartString): contentEnd] )
        
    @commands.hybrid_command(name="мудрость", description="Случайная мудрость", with_app_command=True)
    @discord.app_commands.guilds(discord.Object(id = guildId))
    async def getWisdom(self, ctx: commands.Context):
        """
        Gets random wisdom from randstuff.ru
        """
        
        await ctx.defer()
        
        #all page text
        content = HttpRequestManager.getRequest(HttpCog._wisdomUrl)
        
        simpleLog("HTTP", f"User {ctx.author.name} (ID: {ctx.author.id}) getting random wisdom.")
        
        if content.statusCode != 200:
            #something wrong with host
            errorLog("HTTP", "Can't get random wisdom. REASON: response code from api is not 200")
            await ctx.reply("Чето не так с сайтиком", ephemeral = True)
            return
        
        #find content div start
        contentStart = content.answer.find(HttpCog.randStuffContentStartString)
        #find content div end based on content start
        contentEnd = content.answer.find(HttpCog.randStuffContentEndWisdom, contentStart)
        
        #fact is page text slice where content start is slice start and content end is slice end
        await ctx.reply( content.answer[contentStart + len(HttpCog.randStuffContentStartString): contentEnd] )
        
    @commands.hybrid_command(name="анекдот", description="Случайный анекдот", with_app_command=True)
    @discord.app_commands.guilds(discord.Object(id = guildId))
    async def getJoke(self, ctx: commands.Context):
        """
        Gets random joke from castlots.org
        """
        
        await ctx.defer()
        
        simpleLog("HTTP", f"User {ctx.author.name} (ID: {ctx.author.id}) getting random joke.")
        
        headers = HttpRequestManager.getHeaders("castlots.org", "http://castlots.org", "http://castlots.org/generator-anekdotov-online/")
        
        answer = HttpRequestManager.postRequest(HttpCog._castlotsUrl, headers)
        
        if not answer:
            #something wrong with host
            errorLog("HTTP", "Can't get random wisdom. REASON: api is not responding.")
            await ctx.reply("Чето не так", ephemeral=True)
            return
        
        await ctx.reply(answer['va'])