# sbSounds.py
# 
# Description: 
# The class sbSounds is defined here 
# This file loads the sounds and plays them back.
# 

from ast import Load
from functools import partial, partialmethod
import sys   # System-specific parameters and functions
import os    # Miscellaneous operating system interfaces
import subprocess
import time

import pygame # for audio files

from configSetttingsBase import ConfigSettingsBase

# SoundConfig description: Holds all the settings 
# Instantiation Syntax: SoundConfig()
class SoundSettingsConfig(ConfigSettingsBase):
    # Customize the current instance to a specific initial state.
    def __init__(self):
        # Execute the a base classes __init__() 
        super().__init__("SoundSettings")

        # Define settings and default values
        self.Directory_Red_Sounds = self._addConfigSetting("Directory_Red_Sounds", "red_sounds")
        self.Directory_Blue_Sounds = self._addConfigSetting("Directory_Blue_Sounds", "blue_sounds")
        self.Volume_Percent_Normal = self._addConfigSetting("Volume_Percent_Normal", "100%")
        self.Volume_Sound_Test = self._addConfigSetting("Volume_Sound_Test", "30%")
        #self._configSettings[""] = 


# sbSounds: Loads and Plays the sounds for the Scoreboard.
# Instantiation Syntax: SBsounds()
class sbSounds:
    # Customize the current instance to a specific initial state.
    def __init__(self):
        # Init Sound Ssettings
        self.settings = SoundSettingsConfig()
        self._Sounds = {}

    def loadSoundsFromDirectory(self,  directoryName) -> None:
        """Loads the sounds from the Given directory into _Sounds."""
        if directoryName not in self._Sounds:
            self._Sounds[directoryName] = {}
        for fileName in os.listdir(directoryName):
            self._Sounds[directoryName][fileName] = pygame.mixer.Sound('{}/'.format(directoryName) + fileName)
    
    def getSoundsByGroup(self, groupName) -> dict:
        """Returns a copy of the red sounds dictionary."""
        return self._Sounds[groupName].copy()
    
    def getListSoundsByGroup(self,  groupName) -> list:
        """Returns a list of the red sounds."""
        return list(self._Sounds[groupName])
    
    def getAllSoundsList(self) -> list:
        """Returns a list of all the sounds."""
        allSounds = []
        for sndGroup in self._Sounds.keys():
            allSounds += self._Sounds[sndGroup].values()
        return allSounds

    def setVolume(self, volume) -> None:
        cmd = subprocess.run(["/usr/bin/amixer", "set", "Master", volume])


    def setupSounds(self) -> None:
        """Setup and initialize the sound system."""
        if self.settings.haveSettingBeenLoadedFromConfigFile() or (__name__ == '__main__'):
            pygame.init()
            # Load Red sounds group directory
            print("Loading the red sounds.")
            redGroup = self.settings.Directory_Red_Sounds()
            self.loadSoundsFromDirectory(redGroup)
            self.getRedSounds = partial(self.getSoundsByGroup, redGroup)
            self.getRedSounds.__doc__ = "Returns a copy of the red sounds dictionary."
            self.getRedSoundsList = partial(self.getListSoundsByGroup, redGroup)
            self.getRedSoundsList.__doc__ = "Returns a list of the red sounds."

            print("Loading the blue sounds.")
            blueGroup = str(self.settings.Directory_Blue_Sounds())
            self.loadSoundsFromDirectory(blueGroup)
            self.getRedSounds = partial(self.getSoundsByGroup, blueGroup)
            self.getRedSounds.__doc__ = "Returns a copy of the red sounds dictionary."
            self.getRedSoundsList = partial(self.getListSoundsByGroup, blueGroup)
            self.getRedSoundsList.__doc__ = "Returns a list of the red sounds."

            print("Starting the test for all of the sounds")
            # Set Volume
            self.setVolume(self.settings.Volume_Sound_Test())
            for sound in self.getAllSoundsList():
                sound.play()
                while(pygame.mixer.get_busy()):
                    time.sleep(0.1)
            self.setVolume(self.settings.Volume_Percent_Normal())
            print("Finished the initialization of the red and blue sounds.")

        else:
            raise RuntimeError("Configuration file has not been loaded")

# -----------------------------------------------------------------------------

# Define the "Main Function" which is called automatically if this is the top level Module by the last two lines 
def main() -> int:
    print("Hello World!")

    Sounds = sbSounds()
    Sounds.setupSounds()

    # Return 0 is considered a “successful termination”; anyother value is seen as an error by the OS.)
    return 0 
# End of main() Function  

# Call main function if this is the top level Module 
if __name__ == '__main__':
    sys.exit(main()) 