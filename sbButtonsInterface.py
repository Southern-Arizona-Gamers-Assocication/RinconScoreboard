# sbButtonsInterface.py
# 
# Description: 
# 
#

import sys   # System-specific parameters and functions
#import os    # Miscellaneous operating system interfaces

try:
    # Import Raspberry Pi GPIO library
    import RPi.GPIO as GPIO # pyright: ignore[reportMissingModuleSource]
except ModuleNotFoundError:
    print("Module RPi.GPIO Not Found. Don't use class sbButtonsInterface.")

from configSetttingsBase import ConfigSettingsBase, ConfigSetting, ConfigSettingBool
from processSpawning import SpawnProcess

# SoundConfig description: Holds all the sound settings
# Instantiation Syntax: SoundConfig()
class ButtonsSettingsConfig(ConfigSettingsBase):
    """"""
    _configSection_Name = "Button Settings"

    Scores_File = ConfigSetting("scores.txt")
    GPIO_PinNum_Effect_Red = ConfigSetting(18)
    GPIO_PinNum_Effect_Blue = ConfigSetting(24)
    GPIO_PinNum_Score_Red = ConfigSetting(19)
    GPIO_PinNum_Score_Blue = ConfigSetting(16)
    See_GPIO_Warnings = ConfigSettingBool("No")

# End of class ButtonsSettingsConfig

# Define Functions and Classes Here
class sbButtonsInterface:
    """Class description:
       Instantiation Syntax: className() See __init__() for syntax details.
    """
    def __init__(self) -> None:
        """Customize the current instance to a specific initial state."""
        # Be sure to read current score from file.
        self.score: dict[str, int]= {"red": 0, "blue": 0}
        # These will be assigned to the appropriate functions/methods during setup. Otherwise they do nothing
        self.redEffect_PlaySound = self.dummyMethond
        self.blueEffect_PlaySound = self.dummyMethond
        self.redEffect_LED_Animations = self.dummyMethond
        self.blueEffect_LED_Animations = self.dummyMethond
        self.updateLEDs = self.dummyMethond

    settings = ButtonsSettingsConfig()

    def setupButtons(self) -> None:
        """"""
        self.readScoresFromFile()
        # Setup GPIO for buttons
        GPIO.setmode(GPIO.BCM) # pyright: ignore[reportPossiblyUnboundVariable]
        # Ignore warning for now 
        GPIO.setwarnings(self.settings.See_GPIO_Warnings) # pyright: ignore[reportPossiblyUnboundVariable]

        # Red Effect Button
         # Set GPIO 18 to be an input pin and set initial value to be pulled High (off)
        GPIO.setup(self.settings.GPIO_PinNum_Effect_Red, GPIO.IN, pull_up_down=GPIO.PUD_UP) # pyright: ignore[reportPossiblyUnboundVariable]
        # Setup event on GPIO 18 rising edge
        GPIO.add_event_detect(self.settings.GPIO_PinNum_Effect_Red, # pyright: ignore[reportPossiblyUnboundVariable]
                              GPIO.RISING,                          # pyright: ignore[reportPossiblyUnboundVariable]
                              callback=self.effectRedCallBack,
                              bouncetime=50) 

        # Blue Effect Button
        # Set GPIO 24 to be an input pin and set initial value to be pulled High (off)
        GPIO.setup(self.settings.GPIO_PinNum_Effect_Blue, GPIO.IN, pull_up_down=GPIO.PUD_UP) # pyright: ignore[reportPossiblyUnboundVariable]
        # Setup event on GPIO 24 rising edge
        GPIO.add_event_detect(self.settings.GPIO_PinNum_Effect_Blue, # pyright: ignore[reportPossiblyUnboundVariable]
                              GPIO.RISING,                           # pyright: ignore[reportPossiblyUnboundVariable]
                              callback=self.effectBlueCallBack,
                              bouncetime=50) 

        # Red Score Button
        # Set GPIO 19 to be an input pin and set initial value to be pulled High (off)
        GPIO.setup(self.settings.GPIO_PinNum_Score_Red, GPIO.IN, pull_up_down=GPIO.PUD_UP) # pyright: ignore[reportPossiblyUnboundVariable]
        # Setup event on GPIO 19 rising edge
        GPIO.add_event_detect(self.settings.GPIO_PinNum_Score_Red, # pyright: ignore[reportPossiblyUnboundVariable]
                              GPIO.RISING,                         # pyright: ignore[reportPossiblyUnboundVariable]
                              callback=self.scoreRedCallBack,
                              bouncetime=50) 

        # Blue Score Button
        # Set GPIO 16 to be an input pin and set initial value to be pulled High (off)
        GPIO.setup(self.settings.GPIO_PinNum_Score_Blue, GPIO.IN, pull_up_down=GPIO.PUD_UP) # pyright: ignore[reportPossiblyUnboundVariable]
        # Setup event on GPIO 16 rising edge
        GPIO.add_event_detect(self.settings.GPIO_PinNum_Score_Blue, # pyright: ignore[reportPossiblyUnboundVariable]
                              GPIO.RISING,                          # pyright: ignore[reportPossiblyUnboundVariable]
                              callback=self.scoreBlueCallBack,
                              bouncetime=50) 
    # End of setupButtons() Method

    def effectRedCallBack(self, channel) -> None:
        """"""
        self.redEffect_PlaySound()
        self.redEffect_LED_Animations()
    def effectBlueCallBack(self, channel) -> None:
        """"""
        self.blueEffect_PlaySound()
        self.blueEffect_LED_Animations()

    def scoreRedCallBack(self, channel) -> None:
        """"""
        self.scoreRed += 1
        print(f" Red score: {self.scoreRed}")
        self.writeScoresToFile()
        self.updateLEDs()
    def scoreBlueCallBack(self, channel) -> None:
        """"""
        self.scoreBlue += 1
        print(f"Blue score: {self.scoreBlue}")
        self.writeScoresToFile()
        self.updateLEDs()

    def readScoresFromFile(self) -> None:
        """"""
        inf = open(self.settings.Scores_File,'r').readlines()
        self.score["red"] = int(inf[0].strip())
        self.score["blue"] = int(inf[1].strip())

    def writeScoresToFile(self) -> None:
        """"""
        outf = open(self.settings.Scores_File,'w')
        outf.write(f"{self.score["red"]}\n{self.score["blue"]}\n")
        outf.close()

    def dummyMethond(self) -> None:
        """dummyMethond is just for initializing references to collable objects"""
        pass
# End of class className

# sbButtonsInterfaceMpSpawning() Loads and Plays the sounds for the Scoreboard.
class sbButtonsInterfaceMpSpawning(sbButtonsInterface, SpawnProcess):
    """
    sbButtonsInterfaceMpSpawning() 
    Instantiation Syntax: sbButtonsInterfaceMpSpawning()
    """

    def __init__(self) -> None:
        """"""
        print(f"Executing: sbButtonsInterfaceMpSpawning.__init__()")
        sbButtonsInterface.__init__(self)
        SpawnProcess.__init__(self, "Sounds")
        print(f"Done Executing: sbButtonsInterfaceMpSpawning.__init__()")
        # Setup Sound Effeet Events
        self.eventRedSoundEffect = self.createEvent()
        self.redEffect_PlaySound = self.eventRedSoundEffect.set
        self.eventBlueSoundEffect = self.createEvent()
        self.blueEffect_PlaySound = self.eventBlueSoundEffect.set
        # Setup Light Effeet Events
        self.eventRedLightEffect = self.createEvent()
        self.redEffect_LED_Animations = self.eventRedLightEffect.set
        self.eventBlueLightEffect = self.createEvent()
        self.blueEffect_LED_Animations = self.eventBlueLightEffect.set
        # Setup Score Incriment Queues
        self.queueRedScoreIncriment = self.createQueue()
        self.queueBlueScoreIncriment = self.createQueue()
        self.queueUpdateScores = self.createQueue()

    def scoreRedCallBack(self, channel) -> None:
        """"""
        self.queueRedScoreIncriment.put_nowait(1)
    def scoreBlueCallBack(self, channel) -> None:
        """"""
        self.queueBlueScoreIncriment.put_nowait(1)

    def run_setup(self) -> None:
        """"""
        print(f'{self.name} process is setting up!', flush=True)
        self.setupButtons()

    def run_loop(self) -> None:
        """"""
        if not self.queueRedScoreIncriment.empty() or not self.queueBlueScoreIncriment.empty():
            print("Updating scores.")
            self.flushScoreIncrimentQueue("red", self.queueRedScoreIncriment)
            self.flushScoreIncrimentQueue("blue", self.queueBlueScoreIncriment)
            print()            

    def run_shutdown(self) -> None:
        """"""
        print(f'{self.name} process is shutting down!', flush=True)

    def flushScoreIncrimentQueue(self, c: str, q) -> None:
        for i in range(10):
            if q.empty():
                break
            print(f"  {i} - Incriment {c} score.")
            self.score[c] += q.get_nowait()


# End of class sbButtonsInterfaceMpSpawning

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
    # Clean up
    GPIO.cleanup() # pyright: ignore[reportPossiblyUnboundVariable]
    print(f"blue: {buttons.scoreBlue}, red: {buttons.scoreRed}\n")

    # Return 0 is considered a “successful termination”; anyother value is seen as an error by the OS.)
    return 0 
# End of main() Function  

# Call main function if this is the top level Module 
if __name__ == '__main__':
    sys.exit(main()) 