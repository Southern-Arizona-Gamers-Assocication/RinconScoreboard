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

from configSetttingsBase import ConfigSettingsBase, ConfigSetting, ConfigSettingBool
from processSpawning import SpawnProcess

# Define Functions and Classes Here
class DotStarSettingsConfig(ConfigSettingsBase):
    """DotStarSettingsConfig: Holds all the button settings. Instantiation Syntax: DotStarSettingsConfig()"""
    _configSection_Name = "DotStarLED Settings"

    TotalNumberOfLEDs = ConfigSetting(288)
    LEDOverallBrightness = ConfigSetting(0.1)
    LogFactor = ConfigSetting(14)
# End of class DotStarSettingsConfig

class sbDotStarLEDs:
    """Class description:
       Instantiation Syntax: className() See __init__() for syntax details.
    """
    def __init__(self):
        """Customize the current instance to a specific initial state."""
        self.scoreRed = 0
        self.scoreBlue = 0

    settings = DotStarSettingsConfig()

    def reset_LEDs(self):
        for i in range(self.settings.TotalNumberOfLEDs):
            dots[i] = (0,0,0) # pyright: ignore[reportUndefinedVariable]

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