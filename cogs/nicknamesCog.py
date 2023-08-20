import discord
from discord.ext import commands
from cogs.cog import Cog

from misc.globals import guildId
from misc.utils import memberCanChangeNicknames
from misc.logs import simpleLog, errorLog

class NicknamesCog(Cog):
    """
    Cog that contains all commands that interacting with user nicknames
    """
    
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)
    
    @commands.hybrid_command(name="поставитьник", description="Установить ник пользователю (только для помощников)", with_app_command=True)
    @discord.app_commands.guilds(discord.Object(id = guildId))    
    @discord.app_commands.rename(member="участник", nickname="ник")
    @discord.app_commands.describe(member="участник для смены ника", nickname="новый ник участника")
    async def changeMemberNickname(self, ctx: commands.Context, member: discord.Member, nickname: str):
        """
        sets new nickname to member.
        
        :param member: member for new nickname
        :param nickname: new member's nickname.
        """
        await ctx.defer()
        
        simpleLog("NICKNAMES", f"User {ctx.author.name} (ID: {ctx.author.id}) want to set {member.name} nick to {nickname}")
        
        if not await memberCanChangeNicknames(ctx):
            
            simpleLog("NICKNAMES", f"User {ctx.author.name} (ID: {ctx.author.id}) attempt to set nickname was declined. REASON: User can't change nicknames")
            await ctx.reply("Нет прав для такого действия", ephemeral=True)
            return
        
        await member.edit(nick=nickname)
        await ctx.reply(f"<@{member.id}> теперь {nickname}")
     
    @changeMemberNickname.error
    async def changeNicknameError(self, ctx, error):
        """
        Handles nickname change error.
        """
        errorLog("NICKNAMES", f"Can't change nickname.")
        if isinstance(error, commands.errors.HybridCommandError):
            await ctx.reply("Нет прав для смены ника этому участнику", ephemeral=True)
        else:
            await ctx.reply("Чето не так", ephemeral=True)
     
    @commands.hybrid_command(name="ник", description="Установить себе ник", with_app_command=True)
    @discord.app_commands.guilds(discord.Object(id = guildId))    
    @discord.app_commands.rename(nickname="ник")
    @discord.app_commands.describe(nickname="ваш новый ник")   
    async def selfChangeMemberNickname(self, ctx: commands.Context, nickname: str):
        """
        member nickname change called by himself.
        
        :param nickname: new member's nickname
        """
        await ctx.defer()
        
        simpleLog("NICKNAMES", f"User {ctx.author.name} (ID: {ctx.author.id}) tring to set his nickname to {nickname}")
        
        await ctx.author.edit(nick=nickname)
        
        await ctx.reply(f"Теперь вы {nickname}")
        
    @selfChangeMemberNickname.error
    async def selfChangeError(self, ctx, error):
        """
        Handles self nickname change error.
        """
        errorLog("NICKNAMES", f"Can't change nickname.")
        if isinstance(error, commands.errors.HybridCommandError):
            await ctx.reply("Нет прав. Возможно у вас роль выше чем у бота, либо вы являетесь создателем сервера.", ephemeral=True)
        else:
            await ctx.reply("Чето не так", ephemeral=True)
        
        
        
    
    