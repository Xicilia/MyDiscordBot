import os

from misc.settings import SettingsManager


settings = SettingsManager()
#define guild id here for slash commands
guildId = int(settings.getSetting("serverId"))

