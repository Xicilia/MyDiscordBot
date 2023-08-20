import discord
from discord.ext import commands
from cogs.cog import Cog

import misc.horoCore as horo
from misc.globals import guildId, settings
from misc.utils import getCurrentDateMoscowTimezone
from misc.httpManager import HttpRequestManager
from misc.logs import simpleLog, errorLog

class HoroCog(Cog):
    """
    Cog that contains all comands related to horo
    """
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)
        
    @commands.hybrid_command(name="установитьзнак", description="установить свой знак для использования команды /мойгороскоп")
    @discord.app_commands.guilds(discord.Object(id = guildId))
    @discord.app_commands.rename(sign="знак")
    @discord.app_commands.describe(sign="ваш знак")
    async def setSign(self, ctx:commands.Context, sign:str):
        """
        set members sign.

        :param sign: member sign.
        """
        
        await ctx.defer()
        
        simpleLog("HORO", f"User {ctx.author.name} (ID: {ctx.author.id}) setting sign: {sign}")
        
        result = horo.HoroManager.setMemberHoro(str(ctx.author.id), sign)
        
        if not result:
            await ctx.reply("Чето не так. Возможно знак написан неправильно", ephemeral=True)
            return
        
        await ctx.reply("Знак успешно установлен! Все установленные знаки можно посмотреть командой /знаки", ephemeral=True)

    @commands.hybrid_command(name="знаки", description="Список установленных знаков на сервере")
    @discord.app_commands.guilds(discord.Object(id = guildId))    
    async def getSigns(self, ctx:commands.Context):
        """
        Writes all binded signs.
        """
        
        await ctx.defer()
        
        simpleLog("HORO", f"User {ctx.author.name} (ID: {ctx.author.id}) called signs list.")
        
        signs: dict = settings.getSetting('signs')
        
        message = "Установленные знаки пользователей:\n"
        if len(signs):
            for member in signs.items():
                message += f"<@{member[0]}>: {member[1].capitalize()}\n"
        else:
            message += "Никого нет :("
            
        await ctx.reply(message)
    
    @commands.hybrid_command(name="гороскоп", description="узнать гороскоп на любой знак")
    @discord.app_commands.guilds(discord.Object(id = guildId))
    @discord.app_commands.rename(sign="знак")
    @discord.app_commands.describe(sign="знак на который будет показан гороскоп")        
    async def getHoro(self, ctx: commands.Context, sign: str):
        """
        Gets horo for given sign.
        
        :param sign: sign for horo.
        """
        
        await ctx.defer()
        
        simpleLog("HORO", f"User {ctx.author.name} (ID: {ctx.author.id}) gets horo for sign: {sign}.")
        
        horoObject = horo.HoroManager.getHoro(sign)
        
        if not horoObject:
            
            await ctx.reply("Неправильный знак", ephemeral=True)
            return
        
        horoResponse = HttpRequestManager.getRequest(f"https://1001goroskop.ru/?znak={horoObject['apiName']}")
        
        if horoResponse.statusCode != 200:
            
            errorLog("HORO", "Can't get horo. Reason: response code from api is not 200.")
            await ctx.reply("Чето с сайтиком", ephemeral=True)
            return
        
        #some parsing things
        HoroStart = horoResponse.answer.find("id=\"tomini\"")
        HoroEnd = horoResponse.answer.find("</p>",HoroStart)
        
        horoText = horoResponse.answer[ horoResponse.answer.find("<p>", HoroStart) + 3: HoroEnd ]
        
        await ctx.reply(f"Гороскоп для {horoObject['alias']} на {getCurrentDateMoscowTimezone()}:\n{horoText}\n\n")
        

    @commands.hybrid_command(name="мойгороскоп", description="узнать свой гороскоп (предварительно надо установить знак командой /установитьзнак)")
    @discord.app_commands.guilds(discord.Object(id = guildId))    
    async def getMemberHoro(self, ctx:commands.Context):
        """
        Gets member horo if member have sign (shortcut for getHoro).
        """
        
        memberHoro = horo.HoroManager.getMemberHoro(str(ctx.author.id))
        
        if not memberHoro:
            await ctx.reply("У вас не установлен знак. Чтобы пользоваться командой /мойгороскоп установите знак командой /установитьзнак", ephemeral=True)
            return
        
        await self.getHoro(ctx, memberHoro)