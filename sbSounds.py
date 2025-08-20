# sbSounds.py
# 
# Description: 
# The class sbSounds is defined here 
# This file loads the sounds and plays them back.
# 

from functools import partial, partialmethod
import sys   # System-specific parameters and functions
import os    # Miscellaneous operating system interfaces
import subprocess
import time

try:
    import pygame # for audio files
except ModuleNotFoundError:
    print("Module Pygames Not Found. Don't use class sbSound.")

from configSetttingsBase import ConfigSettingsBase

# SoundConfig description: Holds all the settings 
# Instantiation Syntax: SoundConfig()
class SoundSettingsConfig(ConfigSettingsBase):
    # Customize the current instance to a specific initial state.
    def __init__(self) -> None:
        # Execute the a base classes __init__() 
        super().__init__("SoundSettings")
        print(f"All settings for section: {self.sectionName()}")
        print(self.__configSettings__)

    Directory_Red_Sounds = ConfigSettingsBase.ConfigSetting("red_sounds")
    Directory_Blue_Sounds = ConfigSettingsBase.ConfigSetting("blue_sounds")
    Volume_Percent_Normal = ConfigSettingsBase.ConfigSetting("100%")
    SoundTest_Volume = ConfigSettingsBase.ConfigSetting("30%")
    SoundTest_Wait_for_Sound_End = ConfigSettingsBase.ConfigSettingBool("Yes")
    SoundTest_Print_Sound_Duration  = ConfigSettingsBase.ConfigSettingBool("Yes")
    SoundTest_Sound_Duration_Timeout  = ConfigSettingsBase.ConfigSetting(5.0)
# end of class SoundSettingsConfig

# sbSounds: Loads and Plays the sounds for the Scoreboard.
# Instantiation Syntax: SBsounds()
class sbSounds:
    # Customize the current instance to a specific initial state.
    def __init__(self) -> None:
        # Init Sound Ssettings
        self._Sounds = {}

    settings = SoundSettingsConfig()

    def loadSoundsFromDirectory(self,  directoryName: str) -> None:
        """Loads the sounds from the Given directory into _Sounds."""
        if directoryName not in self._Sounds:
            self._Sounds[directoryName] = {}
        for fileName in os.listdir(directoryName):
            self._Sounds[directoryName][fileName] = pygame.mixer.Sound('{0}/{1}'.format(directoryName, fileName))
    
    def getSoundsByGroup(self, groupName: str) -> dict:
        """Returns a copy of the sounds in the 'groupName' dictionary."""
        return self._Sounds[groupName].copy()
    def getRedSounds(self) -> dict:
        """Returns a copy of the red sounds dictionary."""
        return self.getSoundsByGroup(self.settings.Directory_Red_Sounds)
    def getBlueSounds(self) -> dict:
        """Returns a copy of the blue sounds dictionary."""
        return self.getSoundsByGroup(self.settings.Directory_Blue_Sounds)
    
    def getSoundsListByGroup(self,  groupName: str) -> list:
        """Returns a list of the 'groupName' sounds."""
        return list(self._Sounds[groupName])
    def getRedSoundsList(self) -> list:
        """Returns a list of the red sounds."""
        return self.getSoundsListByGroup(self.settings.Directory_Red_Sounds)
    def getBlueSoundsList(self) -> list:
        """Returns a list of the blue sounds."""
        return self.getSoundsListByGroup(self.settings.Directory_Blue_Sounds)

    def getAllsounds(self) -> dict:
        """Returns a dictionary of all the sounds."""
        return dict(zip(self.getAllSoundsList(), self.getAllSoundsNamesList()))
    
    def getAllSoundsList(self) -> list:
        """Returns a list of all the sounds."""
        allSounds = []
        for sndGroup in self._Sounds.keys():
            allSounds += list(self._Sounds[sndGroup].values())
        return allSounds
    
    def getAllSoundsNamesList(self) -> list[str]:
        """Returns a list of all the sounds."""
        allSoundNames = []
        for sndGroup in self._Sounds.keys():
            for sndNames in self._Sounds[sndGroup].keys():
                allSoundNames.append('{0}/{1}'.format(sndGroup, sndNames))
        return allSoundNames
    
    def playRandomSongFromGroup(self,groupName: str):
        """Plays a radom Song from a group"""

    def setVolume(self, volume: str) -> None:
        cmd = subprocess.run(["/usr/bin/amixer", "set", "Master", volume])

    def testSounds(self) ->None:
        """Tests the sounds and optionally print the times"""
        print("Starting the test for all of the sounds")
        # Set Volume
        self.setVolume(self.settings.SoundTest_Volume)
        for sound, name in self.getAllSoundsList(), self.getAllSoundsNamesList():
            print(f"Playing sound: {name} ", end="")
            sound.play()
            while(pygame.mixer.get_busy()):
                time.sleep(0.1)
            print(">> Duration: ")
        self.setVolume(self.settings.Volume_Percent_Normal)
        print("Finished the initialization of the red and blue sounds.")


    def setupSounds(self) -> None:
        """Setup and initialize the sound system."""
        if self.settings.allSectionSsettingsAreUpdated() or (__name__ == '__main__'):
            #initialize pygame library
            pygame.init()

            # Load Red sounds group directory
            print("Loading the red sounds.")
            self.loadSoundsFromDirectory(self.settings.Directory_Red_Sounds)

            # Load Blue sounds group directory
            print("Loading the blue sounds.")
            self.loadSoundsFromDirectory(self.settings.Directory_Blue_Sounds)

            self.testSounds()
        else:
            raise RuntimeError("Configuration file has not been loaded")
# end of class sbSounds

# -----------------------------------------------------------------------------

# Define the "Main Function" which is called automatically if this is the top level Module by the last two lines 
def main() -> int:
    print("Hello World!")

    sounds = sbSounds()
    sounds.setupSounds()
    sounds.getRedSounds()
    a = sounds.getBlueSoundsList()
    sounds.settings.__isValidConfigFileSettingName__("sdf")
    

    # Return 0 is considered a “successful termination”; anyother value is seen as an error by the OS.)
    return 0 
# End of main() Function  

# Call main function if this is the top level Module 
if __name__ == '__main__':
    sys.exit(main()) 