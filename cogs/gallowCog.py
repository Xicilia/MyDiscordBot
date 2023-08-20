import discord
from discord.ext import commands
from cogs.cog import Cog

from misc.globals import guildId
import misc.gallowCore as gallowCore

from misc.logs import simpleLog, errorLog

class GallowCog(Cog):
    """
    Cog that contains commands for "gallow" game.
    """
    
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)
        
        self._manager = gallowCore.GallowManager(bot)
    
    @commands.hybrid_command(name="виселицастарт", description="Начать виселицу")
    @discord.app_commands.guilds(discord.Object(id = guildId))
    @discord.app_commands.describe(word="Слово виселицы")
    @discord.app_commands.rename(word="слово")
    async def gameStart(self, ctx: commands.Context, word: str):
        """
        starts new gallow game in channel.
        """
        
        simpleLog("GALLOW", f"Attempt to start gallow game on channel (ID: {ctx.channel.id}).")
        
        await ctx.defer()
        
        if not gallowCore.validate(word):
            
            simpleLog("GALLOW", f"Gallow game on channel (ID: {ctx.channel.id}) can't be started. REASON: invalid word.")
            await ctx.reply("Слово содержит некорректные символы. Поддерживается только русский язык", ephemeral=True)
            return
        
        if self._manager.gameExists(ctx.channel.id):
            
            simpleLog("GALLOW", f"Gallow game on channel (ID: {ctx.channel.id}) can't be started. REASON: game already exists.")
            await ctx.reply("В этом канале уже запущена игра", ephemeral=True)
            return
        
        await self._manager.createGame(ctx, word)
        simpleLog("GALLOW", f"Gallow game on channel (ID: {ctx.channel.id}) was started (slow-start).")
        #await interaction.followup.send("Успешно", ephemeral=True)
        
    @commands.hybrid_command(name="виселицастартрандом", description="Начать рандомную виселицу")
    @discord.app_commands.guilds(discord.Object(id = guildId))
    async def gameStartRandom(self, ctx: commands.Context):
        """
        start new game with random word.
        """

        simpleLog("GALLOW", f"Attempt to start random gallow game on channel (ID: {ctx.channel.id}).")

        await ctx.defer()
        
        if self._manager.gameExists(ctx.channel.id):
            
            simpleLog("GALLOW", f"Gallow game on channel (ID: {ctx.channel.id}) can't be started. REASON: game already exists.")
            await ctx.reply("В этом канале уже запущена игра", ephemeral=True)
            return
        
        simpleLog("GALLOW", f"Random gallow game on channel (ID: {ctx.channel.id}) was started.")
        await self._manager.createRandomGame(ctx)
        
    @commands.hybrid_command(name="виселицаначать", description="Начать виселицу принудительно")
    @discord.app_commands.guilds(discord.Object(id = guildId))
    async def gameStartManual(self, ctx: commands.Context):
        """
        start game immediatly if game in this channel exists.
        """
        
        await ctx.defer()
        
        simpleLog("GALLOW", f"Attempt to start gallow game immediatly on channel (ID: {ctx.channel.id}).")
        
        if not self._manager.gameExists(ctx.channel.id):
            
            simpleLog("GALLOW", f"Gallow game on channel (ID: {ctx.channel.id}) can't start immediatly. REASON: no game.")
            await ctx.reply("В этом канале нет начатой игры в виселицу", ephemeral=True)
            return
        
        game = self._manager.getGameByChannelID(ctx.channel.id)
        
        if ctx.author != game.initiator:
            
            simpleLog("GALLOW", f"Gallow game on channel (ID: {ctx.channel.id}) can't start immediatly. REASON: command was called not by initiator.")
            await ctx.reply("принудительно начать виселицу может только инициатор", ephemeral=True)
            return
        
        if not len(game.members):
            
            simpleLog("GALLOW", f"Gallow game on channel (ID: {ctx.channel.id}) can't start immediatly. REASON: no players.")
            await ctx.reply("Нет игроков", ephemeral=True)
            return
        
        await game.startGame()

    @commands.hybrid_command(name="виселицавступить", description="Начать виселицу")
    @discord.app_commands.guilds(discord.Object(id = guildId))
    async def gameJoin(self, ctx:commands.Context):
        """
        joins to game if exists.
        """
        
        await ctx.defer()
        
        simpleLog("GALLOW", f"{ctx.author.name} (ID: {ctx.author.id}) attempting to join gallow game on channel (ID: {ctx.channel.id}).")
        
        if not self._manager.gameExists(ctx.channel.id):
            
            simpleLog("GALLOW", f"{ctx.author.name} (ID: {ctx.author.id}) can't join gallow game on channel (ID: {ctx.channel.id}). REASON: no game.")
            await ctx.reply("В этом канале нет начатой игры в виселицу")
            return
        
        game = self._manager.getGameByChannelID(ctx.channel.id)
        
        if game.started:
            
            simpleLog("GALLOW", f"{ctx.author.name} (ID: {ctx.author.id}) can't join gallow game on channel (ID: {ctx.channel.id}). REASON: game already started.")
            await ctx.reply("Игра уже начата")
            return
        
        await self._manager.addMemberToGame(ctx, game)
    
    @commands.hybrid_command(name="виселицаугадать", description="Начать виселицу")
    @discord.app_commands.guilds(discord.Object(id = guildId))   
    @discord.app_commands.rename(letter="буква")    
    @discord.app_commands.describe(letter="угадываемая буква") 
    async def gameGuess(self, ctx: commands.Context, letter: str):
        """
        guess letter in game.
        """
        
        await ctx.defer()
        
        simpleLog("GALLOW", f"{ctx.author.name} (ID: {ctx.author.id}) guessing letter: {letter} on channel (ID: {ctx.channel.id}).")
        
        if len(letter) != 1:
            
            await ctx.reply("Неправильный формат. Отгадывать нужно одну букву")
            return
        
        if not gallowCore.validate(letter):
            await ctx.reply("Некорректный символ")
            return
        
        if not self._manager.gameExists(ctx.channel.id):
            await ctx.reply("В этом канале нет начатой игры в виселицу")
            return
        
        await self._manager.handleGuessContext(ctx, letter)
        
    