# sbButtonsInterface.py
# 
# Description: 
# 
#

import sys
from time import sleep   # System-specific parameters and functions
import os    # Miscellaneous operating system interfaces

try:
    # Import Raspberry Pi GPIO library
    import RPi.GPIO as GPIO # pyright: ignore[reportMissingModuleSource]
except ModuleNotFoundError:
    print("Module RPi.GPIO Not Found. Don't use class sbButtonsInterface.")

from .configSetttingsBase import ConfigSettingsBase, ConfigSetting, ConfigSettingBool, SubSystemConfigBase
from .processSpawning import SpawnProcess, EventType, QueueType, QueueEmptyException, QueueFullException

# Define Constents Here
BUTTONS_PROCESS_NAME = "Button_Handelers"

# Define Functions and Classes Here
class ButtonsSettingsConfig(ConfigSettingsBase):
    """ButtonsSettingsConfig: Holds all the button settings. Instantiation Syntax: ButtonsSettingsConfig()"""
    _configSection_Name = "Button Settings"

    GPIO_PinNum_Effect_Red = ConfigSetting(18)
    GPIO_PinNum_Effect_Blue = ConfigSetting(24)
    GPIO_PinNum_Score_Red = ConfigSetting(19)
    GPIO_PinNum_Score_Blue = ConfigSetting(16)
    GPIO_See_Warnings = ConfigSettingBool("No")
    Button_Debounce_Time_ms = ConfigSetting(50)
# End of class ButtonsSettingsConfig

class sbButtonsInterface(SubSystemConfigBase):
    """Class description:
       Instantiation Syntax: className() See __init__() for syntax details.
    """
    def __init__(self) -> None:
        """Customize the current instance to a specific initial state."""
        super().__init__()
        # These will be assigned to the appropriate functions/methods during setup. Otherwise they do nothing
        self.redEffect_PlaySound = self.dummyMethond
        self.blueEffect_PlaySound = self.dummyMethond
        self.redEffect_LED_Animations = self.dummyMethond
        self.blueEffect_LED_Animations = self.dummyMethond
        self.redScore_Incriment = self.dummyMethond
        self.blueScore_Incriment = self.dummyMethond
    # End of Method __init__ 

    settings = ButtonsSettingsConfig()

    def setupSubSys(self) -> None:
        """"""
        # Do common setup actions.
        super().setupSubSys()

        # Setup GPIO for buttons
        GPIO.setmode(GPIO.BCM) # pyright: ignore[reportPossiblyUnboundVariable]
        # Ignore warning for now 
        GPIO.setwarnings(self.settings.GPIO_See_Warnings) # pyright: ignore[reportPossiblyUnboundVariable]

        # Red Effect Button
         # Set GPIO 18 to be an input pin and set initial value to be pulled High (off)
        GPIO.setup(self.settings.GPIO_PinNum_Effect_Red, GPIO.IN, pull_up_down=GPIO.PUD_UP) # pyright: ignore[reportPossiblyUnboundVariable]
        # Setup event on GPIO 18 rising edge
        GPIO.add_event_detect(self.settings.GPIO_PinNum_Effect_Red, # pyright: ignore[reportPossiblyUnboundVariable]
                              GPIO.RISING,                          # pyright: ignore[reportPossiblyUnboundVariable]
                              callback=self.effectRedCallBack,
                              bouncetime=self.settings.Button_Debounce_Time_ms) 

        # Blue Effect Button
        # Set GPIO 24 to be an input pin and set initial value to be pulled High (off)
        GPIO.setup(self.settings.GPIO_PinNum_Effect_Blue, GPIO.IN, pull_up_down=GPIO.PUD_UP) # pyright: ignore[reportPossiblyUnboundVariable]
        # Setup event on GPIO 24 rising edge
        GPIO.add_event_detect(self.settings.GPIO_PinNum_Effect_Blue, # pyright: ignore[reportPossiblyUnboundVariable]
                              GPIO.RISING,                           # pyright: ignore[reportPossiblyUnboundVariable]
                              callback=self.effectBlueCallBack,
                              bouncetime=self.settings.Button_Debounce_Time_ms) 

        # Red Score Button
        # Set GPIO 19 to be an input pin and set initial value to be pulled High (off)
        GPIO.setup(self.settings.GPIO_PinNum_Score_Red, GPIO.IN, pull_up_down=GPIO.PUD_UP) # pyright: ignore[reportPossiblyUnboundVariable]
        # Setup event on GPIO 19 rising edge
        GPIO.add_event_detect(self.settings.GPIO_PinNum_Score_Red, # pyright: ignore[reportPossiblyUnboundVariable]
                              GPIO.RISING,                         # pyright: ignore[reportPossiblyUnboundVariable]
                              callback=self.scoreRedCallBack,
                              bouncetime=self.settings.Button_Debounce_Time_ms) 

        # Blue Score Button
        # Set GPIO 16 to be an input pin and set initial value to be pulled High (off)
        GPIO.setup(self.settings.GPIO_PinNum_Score_Blue, GPIO.IN, pull_up_down=GPIO.PUD_UP) # pyright: ignore[reportPossiblyUnboundVariable]
        # Setup event on GPIO 16 rising edge
        GPIO.add_event_detect(self.settings.GPIO_PinNum_Score_Blue, # pyright: ignore[reportPossiblyUnboundVariable]
                              GPIO.RISING,                          # pyright: ignore[reportPossiblyUnboundVariable]
                              callback=self.scoreBlueCallBack,
                              bouncetime=self.settings.Button_Debounce_Time_ms) 
    # End of setupSubSys Method

    def effectRedCallBack(self, channel = 0) -> None:
        """"""
        self.redEffect_PlaySound()
        self.redEffect_LED_Animations()
    def effectBlueCallBack(self, channel = 0) -> None:
        """"""
        self.blueEffect_PlaySound()
        self.blueEffect_LED_Animations()

    def scoreRedCallBack(self, channel = 0) -> None:
        """"""
        self.redScore_Incriment()
    def scoreBlueCallBack(self, channel = 0) -> None:
        """"""
        self.blueScore_Incriment()

    def dummyMethond(self) -> None:
        """dummyMethond is just for initializing references to collable objects"""
        pass

    def shutdownSubSys(self) -> None:
        """"""
        # Clean up
        GPIO.cleanup() # pyright: ignore[reportPossiblyUnboundVariable]
        super().shutdownSubSys()
# End of class sbButtonsInterface

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
        SpawnProcess.__init__(self, BUTTONS_PROCESS_NAME)
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
        self.redScore_Incriment = self.queueRedScoreIncriment.put
        self.queueBlueScoreIncriment = self.createQueue()
        self.blueScore_Incriment = self.queueBlueScoreIncriment.put
        print(f"Done Executing: sbButtonsInterfaceMpSpawning.__init__()")
    # End of Method __init__ 

    def scoreRedCallBack(self, channel = 0) -> None:
        """"""
        try:
            self.queueRedScoreIncriment.put(1, True, 0.01)
        except QueueFullException:
            print(f"{self.nameAndPID} queueRedScoreIncriment has been blocked for 10ms! Somthing is wrong Shutingdown.", flush=True)
            self.exitAllProcesses.set()

    def scoreBlueCallBack(self, channel = 0) -> None:
        """"""
        try:
            self.queueBlueScoreIncriment.put(1, True, 0.01)
        except QueueFullException:
            print(f"{self.nameAndPID} queueBlueScoreIncriment has been blocked for 10ms! Somthing is wrong Shutingdown.", flush=True)
            self.exitAllProcesses.set()

    def run_setup(self) -> bool:
        """run_setup() is called when run() is starting before the "while True" Loop.
            run_setup() returns True to call run_loop() from the "while True" Loop or False to block while waiting for the exit all events to be set. 
            Override this to do somethign usefull."""
        """"""
        print(f"(Parent's PID: {os.getppid()}){self.nameAndPID} process is done setting up!", flush=True)
        self.setupSubSys()
        return False # The "while True" Loop will not run.

    def run_shutdownMustRun(self) -> None:
        """"""
        self.shutdownSubSys()
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
    sounds.setupSubSys()

    buttons = sbButtonsInterface()
    buttons.setupSubSys()
    buttons.redEffect_PlaySound = sounds.playRandomRedSong
    buttons.blueEffect_PlaySound = sounds.playRandomBlueSong

    message = input("Press enter to quit\n\n") # Run until someone presses enter
    # Clean up
    buttons.shutdownSubSys()

    # Return 0 is considered a “successful termination”; anyother value is seen as an error by the OS.)
    return 0 
# End of main() Function  

# Call main function if this is the top level Module 
if __name__ == '__main__':
    sys.exit(main()) 