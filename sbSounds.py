# sbSounds.py
# 
# Description: 
# The class sbSounds is defined here 
# This file loads the sounds and plays them back.
# 

from logging import shutdown
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
from processSpawning import SpawnProcess, cast as CastType, Final
from sbButtonsInterface import BUTTONS_PROCESS_NAME, sbButtonsInterfaceMpSpawning

# Define Constents Here
SOUNDS_CONFIG_SECTION_NAME = "Sound Settings"
SOUNDS_PROCESS_NAME = "Sound_Effects"

# Define Functions and Classes Here
class SoundSettingsConfig(ConfigSettingsBase):
    """SoundConfig: Holds all the sound settings. Instantiation Syntax: SoundSettingsConfig()"""
    _configSection_Name: Final[str] = SOUNDS_CONFIG_SECTION_NAME

    Directory_Red_Sounds = ConfigSetting("red_sounds")
    Directory_Blue_Sounds = ConfigSetting("blue_sounds")
    Volume_Percent_Normal = ConfigSetting("50%")
    Sounds_FadeIn_ms  = ConfigSetting(200)
    SoundTest_Volume = ConfigSetting("20%")
    SoundTest_Play_Timeout_Enable = ConfigSettingBool("Yes")
    SoundTest_Sound_Timeout_ms  = ConfigSetting(2000)
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
        self.soundCounts: dict[str, int] = {}
        self.totalNumOfAllSounds: int = 0
        self.soundDurations: dict[str, dict[str, float]] = {}
        self.soundDurationTotals: dict[str, float] = {}
        self.totalDurationOfAllSounds: float = float(0)
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
    
    def playSound(self, sound, maxPlayTime: float = 0):
        """
        playSound(): Executes pygame.mixer.Sound.play(loops=0, maxtime=0, fade_ms=0) -> Channel
        
        :param sound: The sound object to be played
        :type sound: pygame.mixer.Sound
        :param maxPlayTime: The maxtime argument can be used to stop playback after a given number of milliseconds.
        :type maxPlayTime: float
        """
        sound.play(0,maxPlayTime,self.settings.Sounds_FadeIn_ms)

    def playRandomSongFromGroup(self,groupName: str):
        """Plays a radom song from a group if no other sound is playing."""
        if  (not pygame.mixer.get_busy()): # pyright: ignore[reportPossiblyUnboundVariable]
            sndName = random.choice(list(self._Sounds[groupName]))
            #self._Sounds[groupName][sndName].play()
            self.playSound(self._Sounds[groupName][sndName])
            print(f"Playing sound: {sndName}", flush=True)
    def playRandomRedSong(self):
        """Plays a radom red sound."""
        self.playRandomSongFromGroup(self.settings.Directory_Red_Sounds)
    def playRandomBlueSong(self):
        """Plays a radom blue song."""
        self.playRandomSongFromGroup(self.settings.Directory_Blue_Sounds)

    def setVolume(self, volume: str) -> None:
        cmd = subprocess.run(["/usr/bin/amixer", "set", "Master", volume])
        sleep(0.2)

    def UpdateSoundCounts(self) -> None:
        """"""
        for sndGroup in self.soundDurations:
            self.soundCounts[sndGroup] = len(self.soundDurations[sndGroup])
            self.soundDurationTotals[sndGroup] = sum(self.soundDurations[sndGroup].values())
        self.totalNumOfAllSounds = sum(self.soundCounts.values())
        self.totalDurationOfAllSounds = sum(self.soundDurationTotals.values())
        

    def loadSoundsFromDirectory(self,  directoryName: str) -> None:
        """Loads the sounds from the Given directory into _Sounds."""
        print(f"Loading the sounds from ./{directoryName}...", end=" ")
        self._Sounds[directoryName] = {}
        self.soundDurations[directoryName] = {}
        for fileName in os.listdir(directoryName):
            name = f"{directoryName}/{fileName}"
            snd = pygame.mixer.Sound(name) # pyright: ignore[reportPossiblyUnboundVariable]
            self._Sounds[directoryName][name] = snd
            self.soundDurations[directoryName][name] = snd.get_length() # Return the length of this Sound in seconds.
        self.UpdateSoundCounts()
        print(f"Done! Loaded {self.soundCounts[directoryName]} sounds with {self.soundDurations[directoryName]} seconds of play time.")
    
    def testSounds(self) ->None:
        """Tests the sounds and optionally print the times"""
        print("Starting the test for all of the sounds")
        # Set Volume
        self.setVolume(self.settings.SoundTest_Volume)
        for (name,sound) in self.getAllsounds().items():
            print(f"Playing sound: {name} ", end="")
            if self.settings.SoundTest_Play_Timeout_Enable:
                self.playSound(sound, self.settings.SoundTest_Sound_Timeout_ms)
            else:
                self.playSound(sound)
            while(pygame.mixer.get_busy()): # pyright: ignore[reportPossiblyUnboundVariable]
                sleep(0.1)
            print(">> Duration: ", flush=True)
        self.setVolume(self.settings.Volume_Percent_Normal)
        print("Finished the initialization of the red and blue sounds.", flush=True)

    def setupSounds(self) -> None:
        """Setup and initialize the sound system."""
        #initialize pygame library
        pygame.init() # pyright: ignore[reportPossiblyUnboundVariable]

        # Load Red sounds group directory
        print(f"Loading the sounds from ./{self.settings.Directory_Red_Sounds}...", end=" ")
        self.loadSoundsFromDirectory(self.settings.Directory_Red_Sounds)
        print(f"Done. Loaded {self.soundCounts}")

        # Load Blue sounds group directory
        print("Loading the sounds blue sounds.")
        self.loadSoundsFromDirectory(self.settings.Directory_Blue_Sounds)
        print(f"Done loading sounds. Total Sounds: {self.totalNumOfAllSounds} with {self.totalDurationOfAllSounds} seconds of play time.")

        # Test Sounds 
        self.testSounds()
    # End of Method setupSounds 

    def setupSubSys(self) -> None:
        """Setup and initialize the sound system."""
        # Call this here because no SubSystem specific presetup is needed
        self.preSetupPostSettingsUpdateGetExternalData()
        # Do common setup actions.
        super().setupSubSys()
        self.setupSounds()

    def shutdownSubSys(self) -> None:
        """Runs pygame.mixer.quit() which will uninitialize pygame.mixer. All playback will stop and any 
            loaded Sound objects may not be compatible with the mixer if it is reinitialized later."""
        print("sBSounds is shuting down and uninitialize pygame.mixer.")
        pygame.mixer.quit() # pyright: ignore[reportPossiblyUnboundVariable]
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

    def preStartSetup(self) -> None:
        """preStartSetup() needs to be run before start is called and after the other SpawnProcess instances are initialized.
            Override this to do somethign usefull."""
        self.preSetupPostSettingsUpdateGetExternalData()
        buttonsProcess = CastType(sbButtonsInterfaceMpSpawning, self.getInstancesByProcessName()[BUTTONS_PROCESS_NAME])
        self.assignEventsSoundEffects(buttonsProcess.eventRedSoundEffect, buttonsProcess.eventBlueSoundEffect)
        print(f"{self.name} process is done with pre Start setup.")

    def isReadyToStart(self) -> bool:
        """Checks to see if the red and blue effect events have been assigned.
            IF Overriding, this Method NEEDS to be called. Ex 'super().isReadyToStart()'."""
        readyToStart = True
        if not self.isReadyToSetup():
            print(f"{self.name}.isReadyToSetup() returned false. Hint Has the config file been loaded? ")
            readyToStart = False
        if not super().isReadyToStart():
            readyToStart = False
        if not hasattr(self, "eventRedEffect"):
            print(f"{self.name} is not ready to start because: Assignment of eventRedEffect has not occurred.")
            readyToStart = False
        if not hasattr(self, "eventBlueEffect"):
            print(f"{self.name} is not ready to start because: Assignment of eventBlueEffect has not occurred.")
            readyToStart = False
        return readyToStart
    
    def setupSubSys(self) -> None:
        """Setup and initialize the sound system."""
        # Do common setup actions.
        super().setupSubSys()
        self.setupSounds()

    def run_setup(self) -> bool:
        """Setup Sounds"""
        print(f"{self.nameAndPID} process is setting up!", flush=True)
        if not hasattr(self, "eventRedEffect"):
            raise AttributeError(f"{self.nameAndPID}: Assignment of eventRedEffect has not occurred.")
        if not hasattr(self, "eventBlueEffect"):
            raise AttributeError(f"{self.nameAndPID}: Assignment of eventBlueEffect has not occurred.")
        self.setupSubSys()
        print(f"{self.nameAndPID} process is Done setting up!", flush=True)
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

    def run_shutdownMustRun(self) -> None:
        """run_shutdownMustRun() is called in run()'s try:finally statement so it is always executed.
            This method should only have important resource freeing expressions."""
        self.shutdownSubSys()
# End of class sbSoundsMpSpawning

# -----------------------------------------------------------------------------

# Define the "Main Function" which is called automatically if this is the top level Module by the last two lines 
def main() -> int:
    print("Hello World!")

    #sounds = sbSoundsMpSpawning()
    sounds = sbSounds()
    try:
        sounds.setupSubSys()
        sounds.playRandomRedSong()
        sounds.playRandomBlueSong()
    finally:
        sounds.shutdownSubSys()

    # Return 0 is considered a “successful termination”; anyother value is seen as an error by the OS.)
    return 0 
# End of main() Function  

# Call main function if this is the top level Module 
if __name__ == '__main__':
    sys.exit(main()) 