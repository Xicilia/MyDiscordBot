from misc.globals import settings

def validMask(mask:str) -> bool:

    if not '{sender}' in mask or not '{subject}' in mask or '{comment}' in mask:
        return False
    
    return True

class RPCommand:
    
    def __init__(self, name:str, mask:str):
        
        
        self.name = name
        
        self.mask = mask
        
    def compileCommand(self, sender:str, commandSubject:str, comment:str = ""):
        
        return self.mask.replace('{sender}', sender).replace('{subject}', commandSubject).replace(" {comment}", comment)
        

class RPCommandsManager:
    
    def __init__(self):
        
        self._commands: list[RPCommand] = []
        self.loadCommands()
    
    def getAllCommands(self) -> list[RPCommand]:
        return self._commands
         
    def getRPCommand(self, commandName:str) -> RPCommand:
        
        for command in self._commands:
            
            if command.name.lower() == commandName.lower():
                return command
            
        return None
    
    def getRPListStr(self) -> str:
        commandsList = ""
        
        for command in self._commands:
            commandsList += f'!{command.name}\n'
        
        if not len(commandsList):
            return "Пусто"    
        return commandsList
    
    def loadCommands(self):
        
        commands = settings.getSetting("roleplayCommands")

        for command in commands:
            
            self._commands.append(RPCommand(command['name'], command['mask']))

    def updateCommandsFile(self) -> bool:
        
        commandsList = []
        
        for command in self._commands:
            commandsList.append({
                'name': command.name,
                'mask': command.mask
            })
                    
        settings.setSetting("roleplayCommands", commandsList)
    
    def addCommand(self, name:str, mask:str) -> bool:
        
        if self.isRPCommand(name):
            return False
        
        self._commands.append(RPCommand(name, mask))
        self.updateCommandsFile()
        return True
        
    def removeCommand(self, name:str) -> bool:
        
        command = self.isRPCommand(name)
        
        if not command:
            return False
        
        self._commands.remove(command)
        self.updateCommandsFile()
        return True