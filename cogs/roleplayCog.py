"""
This thing i wrote long time ago and dont want to rewrite so codestyle may be bit different
"""

from discord.ext import commands
from cogs.cog import Cog

from misc.utils import messageIsPing, findUserFromPing
from misc.RPCore import RPCommandsManager
from misc.logs import simpleLog

class RPCog(Cog):
    
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)
        
        self._rpManager = RPCommandsManager()
        
        rpCommands = self._rpManager.getAllCommands()
        
        for command in rpCommands:
            
            #create new command decorator with name as rp command name
            newAction = commands.command(command.name)
            
            #add decorated rp action to commands list
            self.bot.add_command(newAction(self.rpAction))
    
    async def rpAction(self, ctx: commands.Context, firstParameter: str, *otherContent: str):
        """
        Performs rp action.
        """

        #idk why but when i tried to use one parameter as command parameters discord dont saw it
        #so i was forced to split parameters into two arguments and it will cause some extra logic
        
        simpleLog("RP", f"User {ctx.author.name} (ID: {ctx.author.id}) performs rp command: {ctx.command.name}")
        
        if not firstParameter: 
            await ctx.reply("Для того чтобы использовать рп-команду нужно указать человека :nerd:")
            return
        
        command = self._rpManager.getRPCommand(ctx.command.name)
        
        #contains all commands parameters
        splittedMessageContent = [firstParameter, *otherContent]
        
        #find where users section starts and ends
        userSectionStart = -1
        userSectionEnd = -1
        
        users = ""
        comment = ""
        
        userSectionContainsBot = False
         
        for i in range(len(splittedMessageContent)):
            
            currentMessageSliceContent = splittedMessageContent[i]
            
            if messageIsPing(currentMessageSliceContent):
                
                users += currentMessageSliceContent + " " #space for future users
                
                user = await findUserFromPing(self.bot, currentMessageSliceContent)
                
                if user == self.bot.user:
                    userSectionContainsBot = True
                
                if userSectionStart == -1: userSectionStart = i #if user section start wasnt found already - here's start
                
            else:
                
                if userSectionStart != -1: #if user section was found - here's end
                    
                    userSectionEnd = i
                    break
                
        if userSectionStart == -1: #no users in command
            
            await ctx.reply("Не на кого применять команду")
            return
        
        if userSectionStart != 0: #command contains comment
            
            #everything before user section is command comment
            #also add empty string for space for comment
            comment = " ".join(["", *splittedMessageContent[:userSectionStart]])
            
        commandText = command.compileCommand(f"<@{ctx.author.id}>", users.strip(), comment)
        
        if userSectionEnd != -1: #command has quote
            
            commandText = f"{commandText.strip()} с репликой: \"{' '.join(splittedMessageContent[userSectionEnd:])}\""
        
        await ctx.reply(commandText)
        
        if userSectionContainsBot:
            await ctx.message.add_reaction("😻")