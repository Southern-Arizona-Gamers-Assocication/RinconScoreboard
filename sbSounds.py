# sbSounds.py
# 
# Description: 
# The class sbSounds is defined here 
# This file loads the sounds and plays them back.
# 

import sys   # System-specific parameters and functions
import os    # Miscellaneous operating system interfaces
import subprocess
import time
import random


try:
    # for audio files 
    import pygame # pyright: ignore[reportMissingImports]
except ModuleNotFoundError:
    print("Module pygame Not Found. Don't use class sbSound.")

import configSetttingsBase as cb
from processSpawning import SpawnProcess

# SoundConfig description: Holds all the sound settings
# Instantiation Syntax: SoundConfig()
class SoundSettingsConfig(cb.ConfigSettingsBase):
    """"""
    __configSection_Name__ = "Sound Settings"

    Directory_Red_Sounds = cb.ConfigSetting("red_sounds")
    Directory_Blue_Sounds = cb.ConfigSetting("blue_sounds")
    Volume_Percent_Normal = cb.ConfigSetting("50%")
    SoundTest_Volume = cb.ConfigSetting("20%")
    SoundTest_Wait_for_Sound_End = cb.ConfigSettingBool("Yes")
    SoundTest_Print_Sound_Duration  = cb.ConfigSettingBool("Yes")
    SoundTest_Sound_Duration_Timeout  = cb.ConfigSetting(5.0)
# End of class SoundSettingsConfig

# sbSounds() Loads and Plays the sounds for the Scoreboard.
class sbSounds:
    """
    sbSounds() Loads and Plays the sounds for the Scoreboard.
    Instantiation Syntax: SBsounds()
    """
    def __init__(self) -> None:
        """Init Sound subsystem"""
        print(f"Executing: {self.__class__.__qualname__}.__init__()")
        self._Sounds: dict[str, dict[str, pygame.mixer.Sound]] = {} # pyright: ignore[reportPossiblyUnboundVariable]
        self._totalNumOfSounds = 0

    settings = SoundSettingsConfig()

    def loadSoundsFromDirectory(self,  directoryName: str) -> None:
        """Loads the sounds from the Given directory into _Sounds."""
        self._Sounds[directoryName] = {}
        for fileName in os.listdir(directoryName):
            name = f"{directoryName}/{fileName}"
            self._Sounds[directoryName][name] = pygame.mixer.Sound(name) # pyright: ignore[reportPossiblyUnboundVariable]
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
        if  (not pygame.mixer.get_busy()): # pyright: ignore[reportPossiblyUnboundVariable]
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
        time.sleep(0.2)

    def testSounds(self) ->None:
        """Tests the sounds and optionally print the times"""
        print("Starting the test for all of the sounds")
        # Set Volume
        self.setVolume(self.settings.SoundTest_Volume)
        for (name,sound) in self.getAllsounds().items():
            print(f"Playing sound: {name} ", end="")
            sound.play()
            while(pygame.mixer.get_busy()): # pyright: ignore[reportPossiblyUnboundVariable]
                time.sleep(0.1)
            print(">> Duration: ")
        self.setVolume(self.settings.Volume_Percent_Normal)
        print("Finished the initialization of the red and blue sounds.")


    def setupSounds(self) -> None:
        """Setup and initialize the sound system."""
        if self.settings.areSectionSsettingsUpdated() or (__name__ != 'scoreboard.py'):
            #initialize pygame library
            pygame.init() # pyright: ignore[reportPossiblyUnboundVariable]

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

# sbSounds() Loads and Plays the sounds for the Scoreboard.
class sbSoundsMpSpawning(sbSounds, SpawnProcess):
    """
    sbSounds() Loads and Plays the sounds for the Scoreboard.
    Instantiation Syntax: SBsounds()
    """
    def __init__(self) -> None:
        """"""
        print(f"Executing: {self.__class__.__qualname__}.__init__()")
        super(sbSounds).__init__()
        super(SpawnProcess).__init__()
# End of class sbSounds


# -----------------------------------------------------------------------------

# Define the "Main Function" which is called automatically if this is the top level Module by the last two lines 
def main() -> int:
    print("Hello World!")

    sounds = sbSoundsMpSpawning()
    #sounds = sbSounds()
    sounds.setupSounds()
    sounds.playRandomRedSong()
    sounds.playRandomBlueSong()

    # Return 0 is considered a “successful termination”; anyother value is seen as an error by the OS.)
    return 0 
# End of main() Function  

# Call main function if this is the top level Module 
if __name__ == '__main__':
    sys.exit(main()) 