# sbDotStarLEDs.py
# 
# Description: 
# 
#

import sys   # System-specific parameters and functions
#import os    # Miscellaneous operating system interfaces
import math

try:
    # Adafruit board library
    import board  # pyright: ignore[reportMissingImports]
except ModuleNotFoundError:
    print("Module 'board' Not Found. Don't use class sbDotStarLEDs.")
try:
    # Adafruit DotStar library
    import adafruit_dotstar as dotstar  # pyright: ignore[reportMissingImports]
except ModuleNotFoundError:
    print("Module 'adafruit_dotstar' Not Found. Don't use class sbDotStarLEDs.")

from configSetttingsBase import ConfigSettingsBase, ConfigSetting, ConfigSettingBool, SubSystemConfigBase
from processSpawning import SpawnProcess, SharedInteger32, cast as CastType, Final, sleep
from sbButtonsInterface import BUTTONS_PROCESS_NAME, sbButtonsInterfaceMpSpawning
from sbScoreKeeper import SCORE_KEEPER_PROCESS_NAME, sbScoreKeeperMpSpawning

# Define Constents Here
DOT_STAR_LEDS_CONFIG_SECTION_NAME = "DotStar LEDs Settings"
DOT_STAR_LEDS_PROCESS_NAME = "DotStar_LEDs"

# Define Functions and Classes Here
class DotStarSettingsConfig(ConfigSettingsBase):
    """DotStarSettingsConfig: Holds all the button settings. Instantiation Syntax: DotStarSettingsConfig()"""
    _configSection_Name: Final[str] = DOT_STAR_LEDS_CONFIG_SECTION_NAME

    DotStar_Effect_Settings = ConfigSetting("DotStar_Effect_Settings")
    TotalNumberOfLEDs = ConfigSetting(288)
    LEDOverallBrightness = ConfigSetting(0.1)
    LogFactor = ConfigSetting(14)
    LED_Pulsing_Enabled = ConfigSettingBool("No")
    LED_Pulsing_Period = ConfigSetting(2.0)
# End of class DotStarSettingsConfig

class sbDotStarLEDs(SubSystemConfigBase):
    """Class description:
       Instantiation Syntax: className() See __init__() for syntax details.
    """
    def __init__(self):
        """Customize the current instance to a specific initial state."""
        self.setScores(0,0)

    settings = DotStarSettingsConfig()

    def setScores(self, red: int, blue: int) -> None:
        """"""
        self.scoreRed = red
        self.scoreBlue = blue

    def setupSubSys(self) -> None:
        """"""
        # Do common setup actions.
        super().setupSubSys()
        # initialize dots (LEDs) 2 strings of 144 RGB LEDs = 288 LEDs
        self.dots = dotstar.DotStar(board.SCK, board.MOSI, self.settings.TotalNumberOfLEDs, brightness=self.settings.LEDOverallBrightness) # pyright: ignore[reportPossiblyUnboundVariable]
        self.reset_LEDs()
        #self.dots[0] = (0,0,255)
        #self.dots[287] = (255,0,0)
        self.updateLEDsToCurrentScore()

    def updateLEDsToCurrentScore(self) -> None:
        """"""
        self.updateLEDs(self.scoreRed, self.scoreBlue, True)

    def updateLEDs(self, red: int, blue: int, initialize: bool = False):
        """"""
        currBlue = int(math.log(blue) * 14)
        currRed = int(math.log(red) * 14)
        if initialize or currBlue > self.threshold_blue:
            print('Updateing blue LEDSs', flush=True)
            for i in range(currBlue):
                self.dots[i] = (0,0,255)
            self.threshold_blue = currBlue
        if initialize or currRed > self.threshold_red:
            print('Updateing blue LEDSs', flush=True)
            for i in range(288-currRed,288):
                self.dots[i] = (255,0,0)
            self.threshold_red = currRed
        print(f"Number of LED Lights On: red: {currRed}; blue: {currBlue}", flush=True)

    def shutdownSubSys(self) -> None:
        """"""
        # Clean up
        self.reset_LEDs()
        super().shutdownSubSys()


    def reset_LEDs(self) -> None:
        """"""
        self.threshold_red = 0
        self.threshold_blue = 0
        for i in range(self.settings.TotalNumberOfLEDs):
            self.dots[i] = (0,0,0) 
# End of class sbDotStarLEDs

class sbDotStarLEDsMpSpawning(sbDotStarLEDs, SpawnProcess):
    """
    sbDotStarLEDsMpSpawning() 
    Instantiation Syntax: sbDotStarLEDsMpSpawning()
    """

    def __init__(self) -> None:
        """"""
        print(f"Executing: sbDotStarLEDsMpSpawning.__init__()")
        sbDotStarLEDs.__init__(self)
        SpawnProcess.__init__(self, DOT_STAR_LEDS_PROCESS_NAME)
        print(f"Done Executing: sbDotStarLEDsMpSpawning.__init__()")
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
        self.assignEventsSoundEffects(buttonsProcess.eventRedLightEffect, buttonsProcess.eventBlueLightEffect)
        scoreKeeperProcess = CastType(sbScoreKeeperMpSpawning, self.getInstancesByProcessName()[SCORE_KEEPER_PROCESS_NAME])
        self.scoreRedShareing = scoreKeeperProcess.scoreRedShareing.getLink()
        self.scoreBlueShareing = scoreKeeperProcess.scoreBlueShareing.getLink()
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
        if not hasattr(self, "scoreRedShareing"):
            print(f"{self.name} is not ready to start because: Assignment of scoreRedShareing has not occurred.")
            readyToStart = False
        if not hasattr(self, "scoreBlueShareing"):
            print(f"{self.name} is not ready to start because: Assignment of scoreBlueShareing has not occurred.")
            readyToStart = False
        return readyToStart

    def run_setup(self) -> bool:
        """"""
        print(f"{self.nameAndPID} process is setting up!", flush=True)
        self.setScores(self.scoreRedShareing.value, self.scoreBlueShareing.value)
        self.setupSubSys()
        return True

    def run_loop(self) -> bool:
        """run_loop() is called inside run()'s "while True" Loop after checking that the exit event is not set.
            run_loop() returns a True if the default sleep should be used. 
            """
        if self.eventRedEffect.is_set():
            print(f"{self.nameAndPID} Red LED Effect event has been set!", flush=True)
            self.eventRedEffect.clear()
        if self.eventBlueEffect.is_set():
            print(f"{self.nameAndPID} Blue LED Effect event has been set!", flush=True)
            self.eventBlueEffect.clear()
        red = self.scoreRedShareing.value
        blue = self.scoreBlueShareing.value
        if red != self.scoreBlue or blue != self.scoreBlue:
            print(f"{self.nameAndPID} Scores changed! Updating LEDs", flush=True)
            self.setScores(red, blue)
            self.updateLEDsToCurrentScore()
        sleep(0.9)
        return True

    def run_shutdownMustRun(self) -> None:
        """"""
        self.shutdownSubSys()

# End of class sbDotStarLEDsMpSpawning

# -----------------------------------------------------------------------------

# Define the "Main" Function. If this is not the program module this function can be used for isolated debug testing by executing this file.
def main() -> int:
    """This is the "Main" function which is called automatically by the last two lines if this is the top level Module. 'Import this_file' will not call main().
    """
    print("Hello World!")

    # Return 0 is considered a “successful termination”; anyother value is seen as an error by the OS.)
    return 0 
# End of main() Function  

# Call main function if this is the top level Module 
if __name__ == '__main__':
    sys.exit(main()) 