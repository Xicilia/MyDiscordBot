import json

from os.path import isfile
from sys import exit

from misc.logs import simpleLog
from misc.utils import getRootDirectory

from typing import Optional, Any

_emptySettings = {
    
    "botToken": "",

    "commandPrefix": "",

    "sheets": {
        "main": "",
        "reserve": ""
    }
    
}

_settingsFilename = "settings.json"

settingsPrefix = "SETTINGS"

def getSettingsFilePath() -> str:
    return f"{getRootDirectory()}/{_settingsFilename}"

def updateSettingsFile(newSettings: dict) -> bool:
    """
    Updating settings.json with new settings dictionary.
    
    :param newSettings: New settings dictionary.
    
    Returns: True if update was success, else False.
    """
    
    with open(getSettingsFilePath(), 'w', encoding='utf-8') as settingsFile:
        
        json.dump(newSettings, settingsFile, ensure_ascii=False, indent=4, sort_keys=False)


def checkSettingsFile():
    """Checks if settings.json file exists. If not - creates new empty values settings dictionary"""
    
    if not isfile(getSettingsFilePath()):
        
        updateSettingsFile(_emptySettings)
    
    
def parseSettingsFile() -> dict:
    """
    Parses settings.json file.
    
    Returns: dictionary with all settings.
    """
    
    with open(getSettingsFilePath(), 'r', encoding="utf-8") as settingsFile:
        
        try:

            return json.load(settingsFile)
        
        except:
            
            simpleLog(settingsPrefix, "Something wrong with settings file. Check settings.json and restart application.")
            exit()
            

class SettingsManager:
    """
    This class contains info about bot settings and provides easy access to them.
    """
    
    def __init__(self) -> None:
        
        #all settings dictionary
        self._settings: dict = parseSettingsFile()
        
        
    def getSetting(self, settingName:str) -> Optional[Any]:
        """
        Finds and returns setting by it's name.
        
        :param settingName: looking setting name.
        
        Returns: setting value if setting exists, else None
        """
        
        for settingKey in self._settings.keys():
            
            if settingKey == settingName:
                
                return self._settings[settingKey]
            
        #setting is not in settings dictionary
        return None
    
    def addValueToDictionarySetting(self, settingName: str, key: str, value: Any) -> bool:
        """
        adds new value to dictionary setting.
        
        :param settingName: dictionary setting name.
        :param key: key of new setting element.
        :param value: value of new setting element.
        Returns: True if new element was added, else False.
        """
        
        setting: dict = self._settings[settingName]
        
        #if setting is not dictionary object
        if not (type(setting) is dict):
            return False
        
        setting[key] = value
        
        #setting new dictionary to settings.json
        self.setSetting(settingName, setting)
        return True
    
    def setSetting(self, settingName: str, value: Any) -> bool:
        """
        Set setting value.
        
        :param settingName: updating setting name.
        :param value: new setting value.
        
        Returns: True if setting is changed succesfully, else False.
        """
        
        try:
            
            self._settings[settingName] = value
            
            #update settings.json
            updateSettingsFile(self._settings)
            
        except:
            
            simpleLog(settingsPrefix, f"setting \"{settingName}\" is not in settings dictionary.")
            return False