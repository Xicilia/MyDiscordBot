import discord
from discord.ext import commands
from cogs.cog import Cog

from misc.globals import settings, guildId
from misc.utils import numberFormat
from misc.sheetsCore import SheetParser, representValues
from misc.logs import simpleLog

#descirbe for sheet parameter
_sheetDescribe = "Таблица актива (написать слово \"основа\" или \"резерв\")"


class SheetCog(Cog):
    """
    Contains all commands with sheets.
    """
    
    _wrongTableMessage = "Неверная таблица. Принимаются только слова \"Основа\" или \"Резерв\""
    
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)
        
        self.sheets = settings.getSetting("sheets")
        
        self._parser = SheetParser()
        
    @commands.hybrid_command(name="актив", description="Получить актив участника из таблицы", with_app_command=True)
    @discord.app_commands.guilds(discord.Object(id = guildId))
    @discord.app_commands.rename(sheet="таблица", member="участник")
    @discord.app_commands.describe(sheet="Таблица актива (написать слово \"основа\" или \"резерв\")", 
                                   member="Участник, для которого смотрится актив")
    async def getActivity(self, ctx: commands.Context, sheet: str, member: discord.Member):
        """
        Parses given sheet and gets member's activity.
        
        :param sheet: parsing sheet.
        "param member: member in sheet.
        """
        
        await ctx.defer()
        
        simpleLog("SHEETS", f"User {ctx.author.name} (ID: {ctx.author.id}) requests activity. Sheet: {sheet}, member: {member.name}")
        
        if not self._parser.setFrame(sheet.lower()):
            await ctx.reply(SheetCog._wrongTableMessage, ephemeral=True)
            return
            
        entry = self._parser.getActivityByName(member.nick if member.nick else "")
        
        if not entry:
            
            await ctx.reply("Такого участника нет в табличке", ephemeral=True)     
            return       
         
        message = f"Актив {entry.nickname}\n\n"
        
        for i in range(len(entry.activity)):
            
            text = entry.activity[i]
            
            if text == "" or text == "-":
                text = "Нет значения"
            else:
                text = f"{numberFormat(text)} актива"
            
            message += f"{representValues[i]}: {text}\n"
            
        message += f"\nОбщий актив: {numberFormat(entry.fullActivity)} актива\n"   
        
        await ctx.reply(message)
    
    @commands.hybrid_command(name="мойактив", description="Получить свой актив из таблицы (Шорткат команды /актив)")
    @discord.app_commands.guilds(discord.Object(id = guildId))
    @discord.app_commands.rename(sheet="таблица")
    @discord.app_commands.describe(sheet=_sheetDescribe)
    async def getAuthorAcitivty(self, ctx: commands.Context, sheet:str):
        """
        Gets message author's activity (Shortcut for getActivity method).
        
        :param sheet: parsing sheet name.
        """
        
        simpleLog("SHEETS", f"User {ctx.author.name} (ID: {ctx.author.id}) requests his activity. Sheet: {sheet}.")
        
        await self.getActivity(ctx, sheet, ctx.author)
        
    @commands.hybrid_command(name="топ", description="Топ участников по активу")
    @discord.app_commands.guilds(discord.Object(id = guildId))
    @discord.app_commands.rename(sheet="таблица", count="граница")
    @discord.app_commands.describe(sheet=_sheetDescribe, count="Количество отображаемых участников (по умолчанию отображаются все)")
    async def getMembersTopSortedByActivity(self, ctx: commands.Context, sheet: str, count: int = -1):
        """
        Parses given sheet and sorts all members by activity.
        
        :param sheet: sheet name.
        :param count: members count.
        """
        
        await ctx.defer()
        
        simpleLog("SHEETS", f"User {ctx.author.name} (ID: {ctx.author.id}) requests activity top. Sheet: {sheet}, Count: {count}.")
        
        if not self._parser.setFrame(sheet.lower()):
            
            await ctx.reply(SheetCog._wrongTableMessage, ephemeral=True)
            return
        
        entries = self._parser.getMembersSortedByActivity(count)
        
        if not entries:
            
            await ctx.reply("Что-то не так. Скорее всего дело в неправильном значении параметра \"граница\" (должен быть либо больше 1 либо равняться -1)")
            return
        
        #not count because count can be -1
        entriesCount = len(entries)
        
        message = f"Топ-{entriesCount} участников:\n"
        
        for i in range(entriesCount - 1):
            
            currentEntry = entries[i]
            
            message += f"{i + 1}. {currentEntry.nickname} - {currentEntry.fullActivity}\n"
            
        await ctx.reply(message)
    
    @commands.hybrid_command(name="недобор", description="Участники с недобором актива")
    @discord.app_commands.guilds(discord.Object(id = guildId))   
    @discord.app_commands.rename(sheet="таблица", day="день")
    @discord.app_commands.describe(sheet=_sheetDescribe, day="День недели для которого надо найти людей с недобором.")
    async def getWarnableMembers(self, ctx: commands.Context, sheet: str, day:str = "last"):
        """
        Finds warnable members in current sheet for given day.
        
        :param sheet: parsing sheet.
        :param day: day when need to find warnable members.
        """
        
        await ctx.defer()
        
        simpleLog("SHEETS", f"User {ctx.author.name} (ID: {ctx.author.id}) requests warnable members. Sheet: {sheet}. Day: {day}")
        
        if not self._parser.setFrame(sheet.lower()):
            
            await ctx.reply(SheetCog._wrongTableMessage, ephemeral=True)
            return
        
        warnableMembers = self._parser.getWarnableMembers(day)
        
        if not warnableMembers:
            
            await ctx.reply("Чето не так", ephemeral=True)
            return
        
        message = ""
        
        for member in warnableMembers:
            
            message += f"{member.nickname}: недобор {member.activityShortage}\n"
        
        #no warnable members
        if not message:
            message = "Нет никого с предами"
            
        await ctx.reply(message)
            
            
            
    