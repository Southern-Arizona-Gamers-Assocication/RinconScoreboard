# sbDotStarLEDs.py
# 
# Description: 
# 
#

import sys   # System-specific parameters and functions
#import os    # Miscellaneous operating system interfaces

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
from processSpawning import SpawnProcess

# Define Functions and Classes Here
class DotStarSettingsConfig(ConfigSettingsBase):
    """DotStarSettingsConfig: Holds all the button settings. Instantiation Syntax: DotStarSettingsConfig()"""
    _configSection_Name = "DotStarLED Settings"

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
        pass

    settings = DotStarSettingsConfig()

    def setScores(self, red: int, blue: int) -> None:
        """"""
        self.scoreRed = 0
        self.scoreBlue = 0

    def setupSubSys(self) -> None:
        """"""
        # Do common setup actions.
        super().setupSubSys()

        # initialize dots (LEDs) 2 strings of 144 RGB LEDs = 288 LEDs
        self.dots = dotstar.DotStar(board.SCK, board.MOSI, self.settings.TotalNumberOfLEDs, brightness=0.1)
        self.reset_LEDs()
        self.dots[0] = (0,0,255)
        self.dots[287] = (255,0,0)

        threshold_blue = int(math.log(scoreBlue) * 14)
        threshold_red = int(math.log(scoreRed) * 14)
        update_LEDs(initialize = True)

    def shutdownSubSys(self) -> None:
        """"""
        # Clean up
        self.reset_LEDs()
        super().shutdownSubSys()


    def reset_LEDs(self) -> None:
        for i in range(self.settings.TotalNumberOfLEDs):
            self.dots[i] = (0,0,0) 
# End of class sbDotStarLEDs
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