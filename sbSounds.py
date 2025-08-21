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
import random

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

    Directory_Red_Sounds = ConfigSettingsBase.ConfigSetting("red_sounds")
    Directory_Blue_Sounds = ConfigSettingsBase.ConfigSetting("blue_sounds")
    Volume_Percent_Normal = ConfigSettingsBase.ConfigSetting("100%")
    SoundTest_Volume = ConfigSettingsBase.ConfigSetting("30%")
    SoundTest_Wait_for_Sound_End = ConfigSettingsBase.ConfigSettingBool("Yes")
    SoundTest_Print_Sound_Duration  = ConfigSettingsBase.ConfigSettingBool("Yes")
    SoundTest_Sound_Duration_Timeout  = ConfigSettingsBase.ConfigSetting(5.0)
# End of class SoundSettingsConfig

# sbSounds: Loads and Plays the sounds for the Scoreboard.
# Instantiation Syntax: SBsounds()
class sbSounds:
    # Customize the current instance to a specific initial state.
    def __init__(self) -> None:
        # Init Sound Ssettings
        self._Sounds: dict[str, dict[str, pygame.mixer.Sound]] = {}
        self._totalNumOfSounds = 0

    settings = SoundSettingsConfig()

    def loadSoundsFromDirectory(self,  directoryName: str) -> None:
        """Loads the sounds from the Given directory into _Sounds."""
        self._Sounds[directoryName] = {}
        for fileName in os.listdir(directoryName):
            name = f"{directoryName}/{fileName}"
            self._Sounds[directoryName][name] = pygame.mixer.Sound(name)
            self._totalNumOfSounds += 1
    
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
        return list(self._Sounds[groupName].values())
    def getRedSoundsList(self) -> list:
        """Returns a list of the red sounds."""
        return self.getSoundsListByGroup(self.settings.Directory_Red_Sounds)
    def getBlueSoundsList(self) -> list:
        """Returns a list of the blue sounds."""
        return self.getSoundsListByGroup(self.settings.Directory_Blue_Sounds)

    def getAllsounds(self) -> dict:
        """Returns a dictionary of all the sounds."""
        return dict(zip(self.getAllSoundNamesList(), self.getAllSoundsList()))
    
    def getAllSoundsList(self) -> list:
        """Returns a list of all the sounds."""
        allSounds = []
        for sndGroup in self._Sounds.keys():
            allSounds += list(self._Sounds[sndGroup].values())
        return allSounds
    
    def getAllSoundNamesList(self) -> list[str]:
        """Returns a list of all the sounds."""
        allSoundNames: list[str] = []
        for sndGroup in self._Sounds.keys():
            allSoundNames += list(self._Sounds[sndGroup].keys())
        return allSoundNames
    
    def playRandomSongFromGroup(self,groupName: str):
        """Plays a radom song from a group if no other sound is playing."""
        if  (not pygame.mixer.get_busy()):
            sndName = random.choice(list(self._Sounds[groupName].keys()))
            self._Sounds[groupName][sndName].play()
            print(f"Playing sound: {sndName}")
    def playRandomRedSong(self):
        """Plays a radom red sound."""
        self.playRandomSongFromGroup(self.settings.Directory_Red_Sounds)
    def playRandomBlueSong(self):
        """Plays a radom blue song."""
        self.playRandomSongFromGroup(self.settings.Directory_Blue_Sounds)

    def setVolume(self, volume: str) -> None:
        cmd = subprocess.run(["/usr/bin/amixer", "set", "Master", volume])

    def testSounds(self) ->None:
        """Tests the sounds and optionally print the times"""
        print("Starting the test for all of the sounds")
        # Set Volume
        self.setVolume(self.settings.SoundTest_Volume)
        for sound, name in self.getAllSoundsList(), self.getAllSoundNamesList():
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
# End of class sbSounds

# -----------------------------------------------------------------------------

# Define the "Main Function" which is called automatically if this is the top level Module by the last two lines 
def main() -> int:
    print("Hello World!")

    sounds = sbSounds()
    sounds.setupSounds()
    sounds.playRandomRedSong()
    sounds.playRandomBlueSong()

    # Return 0 is considered a “successful termination”; anyother value is seen as an error by the OS.)
    return 0 
# End of main() Function  

# Call main function if this is the top level Module 
if __name__ == '__main__':
    sys.exit(main()) 