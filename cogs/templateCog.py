from discord.ext import commands
from cogs.cog import Cog

class TemplateCog(Cog):
    """
    Cog with some test functions.
    """
    
    def __init__(self, bot: commands.Bot):
        
        super().__init__(bot)
        
    @commands.command(name="пинг")
    async def ping(self, ctx: commands.Context):
        
        await ctx.send("pong")

        