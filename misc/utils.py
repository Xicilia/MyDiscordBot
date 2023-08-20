import datetime
import re
import os

import discord
from discord.ext.commands import Context, Bot

from typing import Optional

from pytz import timezone

def getTimezone():
    return timezone('Europe/Moscow')

def getRootDirectory():
    return os.path.dirname(os.path.abspath(__name__))

def numberFormat(number: int) -> str:
    """
    Formats given number separating thousands by comma
    
    :param number: formatting number.
    Returns: stringified number.
    """
    try:
        number = int(number)
        return "{:,}".format(number)
    except:
        return str(number)
    
def getLastValueIndexInStringifiedList(values: list[str]) -> int:
    """
    Going through list and finds last number index. The reason this function exist is because values in list can be
    separated by empty entries.
    
    :param values: values list.
    Returns: index of last number in list.
    """
    
    lastValueIndex = 0
    
    for i in range(len(values) - 1):
        print(values[i])
        try:
            #attempt to check that value is number
            int(values[i])
            
            #on this step we can say that value is number
            lastValueIndex = i
            
        except ValueError:
            
            continue
        
    return lastValueIndex

def getCurrentDateMoscowTimezone() -> str:
    """
    gets stringified current date in moscow timezone
    """
    
    return datetime.datetime.now(getTimezone()).strftime("%d.%m.%Y")

async def hasRoles(ctx: Context, roles: list[str]) -> bool:
    """
    Finds that ctx author have roles in given list
    
    :param roles: list of roles where at author needs to have at least one role
    Returns: True if author have at least one of given roles, else False
    """
    RoleObjects = []
    
    for role in roles:
        
        RoleObject = discord.utils.find(lambda r: r.name == role, ctx.message.guild.roles)
        
        RoleObjects.append(RoleObject)
    
    for Object in RoleObjects:
        
        if Object in ctx.author.roles: 
            return True
    
    return False

async def memberCanChangeNicknames(ctx: Context) -> bool:
    """
    shortcut for checking that author has role that can change hicknames.
    
    Returns: True if author can change nicknames, else False.
    """
    return await hasRoles(ctx, ["админ сервера", "лидер", "помощник"])

async def memberIsAdmin(ctx: Context) -> bool:
    """
    shortcut for checking that author is admin.
    """
    return await hasRoles(ctx, ['админ сервера'])

async def saveReply(ctx: Context, message:str, embed = None):
    """
    if message length is more than 2000 (discord limit) - split it into chunks and and reply every chunk.
    
    :param message: message which length can be more than 2000
    """
    
    key = 2000
    chunkLimit = 10 #rate limit
    
    if len(message) < key:
        
        await ctx.reply(message, embed=embed)
        
    else:
        
        chunks = []
        
        i = 0
        while i < len(message):
            
            if i+key < len(message):
                
                chunks.append(message[i:i+key])
                
            else:
                
                chunks.append(message[i:len(message)])
                
            i += key
        
        chunksSize = len(chunks)
        
        if chunksSize >= chunkLimit: await ctx.reply("Слишком большое сообщение")
            
        for i in range(chunksSize):
            
            #attach embed only for first chunk
            await ctx.reply(
                chunks[i], embed = embed if i == 0 else None
            )
            
        for chunk in chunks:
            await ctx.reply(chunk)

def messageIsPing(text: str) -> bool:
    """
    Finds that text is user ping or not.
    
    :param text: text that may be ping.
    Returns: True if text is ping, else False.
    """
    
    return re.match(r"<@\d+>", text) != None
            
async def findUserFromPing(bot: Bot, text:str) -> Optional[discord.User]:
    """
    Finds a user from text if it's ping.
    
    :param text: text where user will be found
    Returns: discord.User if user exists, else False
    """
    
    try:
        
        #algorithm finds user based on ping which has <@ID> syntax. We don't need extra symbols so remove first 2 symbols and last symbol
        userId = text[2:][:-1]
        
    except:
        
        #text is not ping
        return None 
    
    try:
        
        user = await bot.fetch_user( int(userId) )
        
        return user
    
    except:
        
        #user dont exist
        return None
    
if __name__ == "__main__":
    
    print(messageIsPing("<@123131231231>"))
    print(messageIsPing("123123"))
    print(messageIsPing("tets"))
    print(messageIsPing("<@test>"))