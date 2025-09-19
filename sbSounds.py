# sbSounds.py
# 
# Description: 
# The class sbSounds is defined here 
# This file loads the sounds and plays them back.
# 

import sys   # System-specific parameters and functions
import os    # Miscellaneous operating system interfaces
import subprocess
from time import sleep
import random


try:
    # Import Sound library to play audio files 
    import pygame # pyright: ignore[reportMissingImports]
except ModuleNotFoundError:
    print("Module pygame Not Found. Don't use class sbSound.")

from configSetttingsBase import ConfigSettingsBase, ConfigSetting, ConfigSettingBool, SubSystemConfigBase
from processSpawning import SpawnProcess, cast 
from sbButtonsInterface import BUTTONS_PROCESS_NAME, sbButtonsInterfaceMpSpawning

# Define Constents Here
SOUNDS_PROCESS_NAME = "Sound_Effects"

# Define Functions and Classes Here
class SoundSettingsConfig(ConfigSettingsBase):
    """SoundConfig: Holds all the sound settings. Instantiation Syntax: SoundSettingsConfig()"""
    _configSection_Name = "Sound Settings"

    Directory_Red_Sounds = ConfigSetting("red_sounds")
    Directory_Blue_Sounds = ConfigSetting("blue_sounds")
    Volume_Percent_Normal = ConfigSetting("50%")
    SoundTest_Volume = ConfigSetting("20%")
    SoundTest_Wait_for_Sound_End = ConfigSettingBool("Yes")
    SoundTest_Print_Sound_Duration  = ConfigSettingBool("Yes")
    SoundTest_Sound_Duration_Timeout  = ConfigSetting(5.0)
# End of class SoundSettingsConfig

# sbSounds() Loads and Plays the sounds for the Scoreboard.
class sbSounds(SubSystemConfigBase):
    """
    sbSounds() Loads and Plays the sounds for the Scoreboard.
    Instantiation Syntax: SBsounds()
    """
    def __init__(self) -> None:
        """Init Sound subsystem"""
        super().__init__()
        print(f"Start Executing: sbSounds.__init__() For class: {self.__class__.__qualname__}")
        self._Sounds: dict[str, dict[str, pygame.mixer.Sound]] = {} # pyright: ignore[reportPossiblyUnboundVariable]
        self._totalNumOfSounds = 0
        print(f"Done Executing: sbSounds.__init__()")
    # End of Method __init__ 

    settings = SoundSettingsConfig()

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
            sndName = random.choice(list(self._Sounds[groupName]))
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
        sleep(0.2)

    def loadSoundsFromDirectory(self,  directoryName: str) -> None:
        """Loads the sounds from the Given directory into _Sounds."""
        self._Sounds[directoryName] = {}
        for fileName in os.listdir(directoryName):
            name = f"{directoryName}/{fileName}"
            self._Sounds[directoryName][name] = pygame.mixer.Sound(name) # pyright: ignore[reportPossiblyUnboundVariable]
            self._totalNumOfSounds += 1
    
    def testSounds(self) ->None:
        """Tests the sounds and optionally print the times"""
        print("Starting the test for all of the sounds")
        # Set Volume
        self.setVolume(self.settings.SoundTest_Volume)
        for (name,sound) in self.getAllsounds().items():
            print(f"Playing sound: {name} ", end="")
            sound.play()
            while(pygame.mixer.get_busy()): # pyright: ignore[reportPossiblyUnboundVariable]
                sleep(0.1)
            print(">> Duration: ")
        self.setVolume(self.settings.Volume_Percent_Normal)
        print("Finished the initialization of the red and blue sounds.")

    def setupSounds(self) -> None:
        """Setup and initialize the sound system."""
        #initialize pygame library
        pygame.init() # pyright: ignore[reportPossiblyUnboundVariable]

        # Load Red sounds group directory
        print("Loading the red sounds.")
        self.loadSoundsFromDirectory(self.settings.Directory_Red_Sounds)

        # Load Blue sounds group directory
        print("Loading the blue sounds.")
        self.loadSoundsFromDirectory(self.settings.Directory_Blue_Sounds)
        # Test Sounds 
        self.testSounds()

    def setupSubSys(self) -> None:
        """Setup and initialize the sound system."""
        # Call this here because no SubSystem specific presetup is needed
        self.preSetupPostSettingsUpdateGetExternalData()
        # Do common setup actions.
        super().setupSubSys()
        self.setupSounds()
# End of class sbSounds

# sbSoundsMpSpawning() Loads and Plays the sounds for the Scoreboard.
class sbSoundsMpSpawning(sbSounds, SpawnProcess):
    """
    sbSoundsMpSpawning() Loads and Plays the sounds for the Scoreboard.
    Instantiation Syntax: sbSoundsMpSpawning()
    """

    def __init__(self) -> None:
        """"""
        print(f"Executing: sbSoundsMpSpawning.__init__()")
        sbSounds.__init__(self)
        SpawnProcess.__init__(self, SOUNDS_PROCESS_NAME)
        print(f"Done Executing: sbSoundsMpSpawning.__init__()")
        if "sbButtonsInterfaceMpSpawning" in globals():
            print("sbSoundsMpSpawning can see the class sbButtonsInterfaceMpSpawning")
        if "configFileParser" in globals():
            print("sbSoundsMpSpawning can see the class configFileParser")
    # End of Method __init__ 

    def assignEventsSoundEffects(self, redEvent, blueEvent) -> None:
        """"""
        self.eventRedEffect = self.assignEvent(redEvent)
        self.eventBlueEffect = self.assignEvent(blueEvent)
        self.run_setup

    def preStartSetup(self) -> None:
        """preStartSetup() needs to be run before start is called and after the other SpawnProcess instances are initialized.
            Override this to do somethign usefull."""
        self.preSetupPostSettingsUpdateGetExternalData()
        buttonsProcess = cast(sbButtonsInterfaceMpSpawning, self.getInstancesByProcessName()[BUTTONS_PROCESS_NAME])
        self.assignEventsSoundEffects(buttonsProcess.eventRedSoundEffect, buttonsProcess.eventBlueSoundEffect)
        print(f'{self.name} process is done with pre Start setup.')

    def isReadyToStart(self) -> bool:
        """Checks to see if the red and blue effect events have been assigned.
            IF Overriding, this Method NEEDS to be called. Ex 'super().isReadyToStart()'."""
        if not self.isReadyToSetup():
            print(f"{self.nameAndPID}.isReadyToSetup() returned false. Hint Has the config file been loaded? ")
            return False
        if not super().isReadyToStart():
            return False
        if not hasattr(self, "eventRedEffect"):
            print(f"{self.nameAndPID}: Assignment of eventRedEffect has not occurred.")
            return False
        if not hasattr(self, "eventBlueEffect"):
            print(f"{self.nameAndPID}: Assignment of eventBlueEffect has not occurred.")
            return False
        return True
    
    def setupSubSys(self) -> None:
        """Setup and initialize the sound system."""
        # Do common setup actions.
        super().setupSubSys()
        self.setupSounds()

    def run_setup(self) -> bool:
        """Setup Sounds"""
        print(f'{self.name} process is setting up!', flush=True)
        if not hasattr(self, "eventRedEffect"):
            raise AttributeError(f"{self.nameAndPID}: Assignment of eventRedEffect has not occurred.")
        if not hasattr(self, "eventBlueEffect"):
            raise AttributeError(f"{self.nameAndPID}: Assignment of eventBlueEffect has not occurred.")
        self.setupSubSys()
        return True
    
    def run_loop(self) -> bool:
        """"""
        if self.eventRedEffect.is_set():
            self.playRandomRedSong()
            self.eventRedEffect.clear()
        if self.eventBlueEffect.is_set():
            self.playRandomBlueSong()
            self.eventBlueEffect.clear()
        return True
# End of class sbSoundsMpSpawning


# -----------------------------------------------------------------------------

# Define the "Main Function" which is called automatically if this is the top level Module by the last two lines 
def main() -> int:
    print("Hello World!")

    sounds = sbSoundsMpSpawning()
    #sounds = sbSounds()
    sounds.setupSubSys()
    sounds.playRandomRedSong()
    sounds.playRandomBlueSong()

    # Return 0 is considered a “successful termination”; anyother value is seen as an error by the OS.)
    return 0 
# End of main() Function  

# Call main function if this is the top level Module 
if __name__ == '__main__':
    sys.exit(main()) 