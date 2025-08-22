# sbButtonsInterface.py
# 
# Description: 
# 
#

import sys   # System-specific parameters and functions
#import os    # Miscellaneous operating system interfaces

try:
    import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
except ModuleNotFoundError:
    print("Module Pygames Not Found. Don't use class sbSound.")

from configSetttingsBase import ConfigSettingsBase

# SoundConfig description: Holds all the sound settings
# Instantiation Syntax: SoundConfig()
class ButtonsSettingsConfig(ConfigSettingsBase):
    # Customize the current instance to a specific initial state.
    def __init__(self) -> None:
        # Execute the a base classes __init__() 
        super().__init__("Button Settings")

    Scores_File = ConfigSettingsBase.ConfigSetting("scores.txt")
    GPIO_PinNum_Effect_Red = ConfigSettingsBase.ConfigSetting(18)
    GPIO_PinNum_Effect_Blue = ConfigSettingsBase.ConfigSetting(24)
    GPIO_PinNum_Score_Red = ConfigSettingsBase.ConfigSetting(19)
    GPIO_PinNum_Score_Blue = ConfigSettingsBase.ConfigSetting(16)
    See_GPIO_Warnings = ConfigSettingsBase.ConfigSettingBool("No")

# End of class SoundSettingsConfig

# Define Functions and Classes Here
class sbButtonsInterface:
    """Class description:
       Instantiation Syntax: className() See __init__() for syntax details.
    """
    def __init__(self):
        """Customize the current instance to a specific initial state."""
        # Be sure to read current score from file.
        self.scoreRed = 0
        self.scoreBlue = 0

        # These will be assigned to the appropriate functions/methods during setup. Otherwise they do nothing
        self.redEffect_PlaySound = self.dummyMethond
        self.blueEffect_PlaySound = self.dummyMethond
        self.redEffect_LED_Animations = self.dummyMethond
        self.blueEffect_LED_Animations = self.dummyMethond
        self.updateLEDs = self.dummyMethond

    settings = ButtonsSettingsConfig()

    def setupButtons(self):
        """"""
        self.readScoresFromFile()
        # Setup GPIO for buttons
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(self.settings.See_GPIO_Warnings) # Ignore warning for now

        # Red Effect Button
        GPIO.setup(self.settings.GPIO_PinNum_Effect_Red, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set GPIO 18 to be an input pin and set initial value to be pulled High (off)
        GPIO.add_event_detect(self.settings.GPIO_PinNum_Effect_Red,
                              GPIO.RISING,
                              callback=self.effectRedCallBack,
                              bouncetime=50) # Setup event on GPIO 18 rising edge

        # Blue Effect Button
        GPIO.setup(self.settings.GPIO_PinNum_Effect_Blue, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set GPIO 24 to be an input pin and set initial value to be pulled High (off)
        GPIO.add_event_detect(self.settings.GPIO_PinNum_Effect_Blue,
                              GPIO.RISING,
                              callback=self.effectBlueCallBack,
                              bouncetime=50) # Setup event on GPIO 24 rising edge

        # Red Score Button
        GPIO.setup(self.settings.GPIO_PinNum_Score_Red, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set GPIO 19 to be an input pin and set initial value to be pulled High (off)
        GPIO.add_event_detect(self.settings.GPIO_PinNum_Score_Red,
                              GPIO.RISING,
                              callback=self.scoreRedCallBack,
                              bouncetime=50) # Setup event on GPIO 19 rising edge

        # Blue Score Button
        GPIO.setup(self.settings.GPIO_PinNum_Score_Blue, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set GPIO 16 to be an input pin and set initial value to be pulled High (off)
        GPIO.add_event_detect(self.settings.GPIO_PinNum_Score_Blue,
                              GPIO.RISING,
                              callback=self.scoreBlueCallBack,
                              bouncetime=50) # Setup event on GPIO 16 rising edge
    # End of setupButtons

    def effectRedCallBack(self, channel):
        """"""
        self.redEffect_PlaySound()
        self.redEffect_LED_Animations()
    def effectBlueCallBack(self, channel):
        """"""
        self.blueEffect_PlaySound()
        self.blueEffect_LED_Animations()

    def scoreRedCallBack(self, channel):
        """"""
        self.scoreRed += 1
        print(f" Red score: {self.scoreRed}")
        self.writeScoresToFile()
        self.updateLEDs()
    def scoreBlueCallBack(self, channel):
        """"""
        self.scoreBlue += 1
        print(f"Blue score: {self.scoreBlue}")
        self.writeScoresToFile()
        self.updateLEDs()

    def readScoresFromFile(self):
        """"""
        inf = open(self.settings.Scores_File,'r').readlines()
        self.scoreRed = int(inf[0].strip())
        self.scoreBlue = int(inf[1].strip())

    def writeScoresToFile(self):
        """"""
        outf = open(self.settings.Scores_File,'w')
        outf.write(f"{self.scoreRed}\n{self.scoreBlue}\n")
        outf.close()

    def dummyMethond(self) -> None:
        """dummyMethond is just for initializing references to collable objects"""
        pass
# End of class className

# -----------------------------------------------------------------------------

# Define the "Main" Function. If this is not the program module this function can be used for isolated debug testing by executing this file.
def main() -> int:
    """This is the "Main" function which is called automatically by the last two lines if this is the top level Module. 'Import this_file' will not call main().
    """
    # Import Local modules here.
    from sbSounds import sbSounds
    print("Import done for local modules.")
    # Setup Done now run tests

    sounds = sbSounds()
    sounds.setupSounds()

    buttons = sbButtonsInterface()
    buttons.setupButtons()
    buttons.redEffect_PlaySound = sounds.playRandomRedSong
    buttons.blueEffect_PlaySound = sounds.playRandomBlueSong

    message = input("Press enter to quit\n\n") # Run until someone presses enter
    GPIO.cleanup() # Clean up
    print(f"blue: {buttons.scoreBlue}, red: {buttons.scoreRed}\n")

    # Return 0 is considered a “successful termination”; anyother value is seen as an error by the OS.)
    return 0 
# End of main() Function  

# Call main function if this is the top level Module 
if __name__ == '__main__':
    sys.exit(main()) 