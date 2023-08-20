import discord
from cogs.cog import Cog
from discord.ext import commands

from misc.globals import guildId
from misc.utils import saveReply
from misc.wildberriesCore import getRandomWildberriesProduct, serializeWildberriesProductToString, serializeWildberriesProductImageToEmbed
from misc.logs import simpleLog, errorLog

class WildberriesCog(Cog):
    
    def __init__(self, bot: commands.Bot):
        
        super().__init__(bot)
        
    @commands.hybrid_command(name="рандомвб", description="Случайный продукт с вайлдберрис", with_app_command=True)
    @discord.app_commands.guilds(discord.Object(id = guildId))
    async def getWBProduct(self, ctx: commands.Context):
        """
        Gets random product using wildberries api.
        """
        
        await ctx.defer()
        
        simpleLog("WILDBERRIES", f"User {ctx.author.name} (ID: {ctx.author.id}) requests random wildberries product.")
        
        #if product will be None 3 times in a row - stop trying to get
        deep = 1
        product = None
        
        while deep < 3:
            
            product = getRandomWildberriesProduct()
            
            if product: break
            
            deep += 1
            
        else:
            errorLog("WILDBERRIES", "Can't get product 3 times.")
            await ctx.reply("Не могу получить продукт, попробуй снова", ephemeral=True)
            
        await saveReply(
            ctx,
            serializeWildberriesProductToString(product),
            serializeWildberriesProductImageToEmbed(product)
        )