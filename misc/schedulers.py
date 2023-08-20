import datetime

from discord.ext import commands, tasks

from random import choice

from os import listdir
from os.path import isfile, join

from misc.globals import settings
from misc.utils import getRootDirectory, getTimezone

_catsFolder = "cats"

_tz = getTimezone()
_timeForSleepMessage = datetime.time(hour=19, minute=20, tzinfo=_tz)
_timeForMorningMessage = datetime.time(hour=7, tzinfo=_tz) 

class ScheduleTasksManager:
    
    def __init__(self, bot: commands.Bot):
        
        self.bot = bot
        
        try:
            self._sleepChannel = int(settings.getSetting("sleepMessagesChannelId"))
        except:
            self._sleepChannel = None
        
    @tasks.loop(minutes=30)
    async def changeAvatar(self):
        """
        Bot will change avatar with random image located in /cats/
        """
        
        pathToCatsFolder = f"{getRootDirectory()}/{_catsFolder}"
        
        newAvatarPath = choice(
            [f for f in listdir(pathToCatsFolder) if isfile(join(pathToCatsFolder, f))]
        )
        
        with open(join(pathToCatsFolder, newAvatarPath), 'rb') as file:
            
            await self.bot.user.edit(avatar = file.read())
    
    @tasks.loop(minutes=1)        
    async def TimeBasedTask(self):
        """
        task will contain all stuff that will require time
        """
            
        now = datetime.datetime.now(_tz).replace(second=0, microsecond=0)
        
        if self._sleepChannel:
            
            if now.time() == _timeForSleepMessage:
                
                await self.bot.get_channel(self._sleepChannel).send("спокойной ночки друзяшки сладких вам снов")
                
            elif now.time() == _timeForMorningMessage:
                
                await self.bot.get_channel(self._sleepChannel).send("доброе утро друзяшки всем удачного дня и хорошего настроения")
            
    def start(self):
        
        self.changeAvatar.start()
        self.TimeBasedTask.start()
        
        
        
        