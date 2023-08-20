from discord.ext import commands

class Cog(commands.Cog):
    """
    Implementation of basic discord cog.
    """
    
    def __init__(self, bot: commands.Bot):

        
        self.bot = bot