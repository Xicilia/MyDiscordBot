"""
This thing i wrote long time ago and dont want to rewrite so it can have different code style than other scripts
"""

import discord
import threading
import time
import asyncio
import requests

ERRORSMAX = 6

availabledsymbols = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

def getRandomWord() -> str:
    
    answer = requests.get('http://free-generator.ru/generator.php?action=word&type=0').json()
    return answer['word']['word']

def validate(inputStr:str) -> bool:
    
    for letter in inputStr.lower():
        if letter not in availabledsymbols:
            return False
        
    return True

class GallowGame:
    
    def __init__(self, bot, manager, channelID:int, initiator:discord.Member, word:str, forAll=False):
        
        self.bot = bot
        self.manager = manager
        
        self.channelID:int = channelID
        
        self.initiator:str = initiator
        
        self.word:str = word
        
        self.guessedLetters:list[str] = []
        
        self.forAll = forAll
        
        self.errors:int = 0
        self.errorLetters:list[str] = []
        
        self.members:list[discord.Member] = []
            
        self.started:bool = False
        if not self.forAll:
            self._startThread = threading.Thread(target=self._slowStartThread)
            self._startThread.daemon = True
            
            self._startThread.start()
    
    def _slowStartThread(self):
        time.sleep(60)
        
        StartLoop = asyncio.run_coroutine_threadsafe(self._slowStart(), self.bot.loop)
        StartLoop.result()                    

    async def _slowStart(self):
        if not len(self.members):
            await self.bot.get_channel(self.channelID).send("Недостаточно участников для начала игры :( :(")
            
            self.manager.removeGame(self)
            
            return
        
        if not self.started:
            await self.startGame()
    
    def getFormattedWord(self):
        
        formattedWord = ""
        for letter in self.word:
            if letter in self.guessedLetters:
                formattedWord += letter
            else:
                formattedWord += "#"
                
        return formattedWord
    
    def getCurrentStateImage(self):
        
        return discord.File(f"gallowassets\\{self.errors}.png")
    
    async def printGameState(self, ctx, guessMessage:str = ""):
        
        errorLettersList = ", ".join([letter for letter in self.errorLetters])
        
        message = f"{guessMessage}\n\nВиселица. Инициатор: <@{self.initiator.id}>.\n\nСлово: {self.getFormattedWord()}\n\nОшибок: {self.errors}\nНеправильные буквы: {errorLettersList}\n\nДля того чтобы угадать букву используйте команду !виселицаугадать"
        
        if ctx:
            await ctx.reply(message, file=self.getCurrentStateImage())
        else:
            await self.bot.get_channel(self.channelID).send(message, file=self.getCurrentStateImage())
    
    async def handleGuess(self, letter: str, member:discord.Member, ctx):
        
        guessMessage = ""
        if letter in self.word:
            
            if letter in self.guessedLetters:
                await ctx.reply("Буква уже отгадана", ephemeral=True)
                return
            
            self.guessedLetters.append(letter)
            
            if self.getFormattedWord() == self.word:
               await ctx.reply(f"Победа! Слово виселицы: \"{self.word}\". Последнюю букву отгадал <@{member.id}>", file=self.getCurrentStateImage()) 
               self.manager.removeGame(self)
               return
            
            #await self.bot.get_channel(self.channelID).send(f"<@{member.id}> предложил букву \"{letter}\". Это верный вариант")
            guessMessage = f"<@{member.id}> предложил букву \"{letter}\". Это верный вариант"
            
        else:
            
            if letter in self.errorLetters:
                await ctx.reply("Букву уже предлагали", ephemeral=True)
                return
            
            self.errorLetters.append(letter)
            self.errors += 1
            
            if self.errors == 6:
                await ctx.reply(f"Поражение :( Слово виселицы: \"{self.word}\"", file=self.getCurrentStateImage())
                self.manager.removeGame(self)
                return
            
            #await self.bot.get_channel(self.channelID).send(f"<@{member.id}> предложил букву \"{letter}\". Это неправильный вариант")
            guessMessage = f"<@{member.id}> предложил букву \"{letter}\". Это неправильный вариант"
            
        await self.printGameState(ctx, guessMessage)
    
    async def startGame(self, ctx = None):
        
        self.started = True
        
        await self.printGameState(ctx)

class GallowManager:
    
    def __init__(self, bot):
        
        self.bot = bot
        
        self.games:list[GallowGame] = []
    
    async def createRandomGame(self, ctx):
        game = GallowGame(self.bot, self, ctx.channel.id, self.bot.user, getRandomWord(), True)
        await game.startGame(ctx)
        self.games.append(game) 
        
        await ctx.reply(f"<@{ctx.author.id}> начал случайную виселицу, учавствовать могут все в канале")
        
    async def createGame(self, ctx, word:str):
        
        self.games.append(GallowGame(self.bot, self, ctx.channel.id, ctx.author, word))    
        
        await ctx.reply(f"<@{ctx.author.id}> начал виселицу. Для того чтобы присоединиться напишите команду /виселицавступить. До старта 60 секунд (начать игру можно принудительно командой /виселицаначать)")

    async def handleGuessContext(self, ctx, letter):
        
        game = self.getGameByChannelID(ctx.channel.id)
        
        if ctx.author == game.initiator:
            await ctx.reply("Это ваша игра зачем угадывать")
            return
        
        if not game.forAll and ctx.author not in game.members:
            await ctx.reply("Вы не учавствуете в игре")
            return
        
        if not game.started:
            await ctx.reply("Игра еще не началась, дождитесь начала")
            return
        
        await game.handleGuess(letter, ctx.author, ctx)
    
    async def addMemberToGame(self, ctx, game):
        
        #game = self.getGameByChannelID(ctx.channel.id)
        
        if not game:
            
            await ctx.reply("Нет активной игры")
            return
        
        if game.initiator == ctx.author:
            
            await ctx.reply("Это ваша игра зачем вступать")
            return
        
        game.members.append(ctx.author)
        await ctx.reply(f"Участник <@{ctx.author.id}> учавствует в игре")
    
    def gameExists(self, channelID:int) -> bool:
        
        for game in self.games:
            
            if game.channelID == channelID:
                return True
            
        return False
    
    def getGameByChannelID(self, channelID:int) -> GallowGame:
        
        for game in self.games:
            
            if game.channelID == channelID:
                return game
            
        return None
    
    def removeGame(self, game):
        self.games.remove(game)
