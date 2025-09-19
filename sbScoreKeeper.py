# sbScoreKeeper.py
# 
# Description: 
# 
#

import sys
from time import sleep   # System-specific parameters and functions
#import os    # Miscellaneous operating system interfaces

from configSetttingsBase import ConfigSettingsBase, ConfigSetting, ConfigSettingBool, SubSystemConfigBase
from processSpawning import SpawnProcess, EventType, QueueType, QueueEmptyException
from sbButtonsInterface import BUTTONS_PROCESS_NAME, sbButtonsInterfaceMpSpawning

# Define Constents Here
SCORE_PROCESS_NAME = "Score_Keeper"

# Define Functions and Classes Here
class ScoreingSettingsConfig(ConfigSettingsBase):
    """ScoreingSettingsConfig: Holds all the button settings. Instantiation Syntax: ScoreingSettingsConfig()"""
    _configSection_Name = "ScoreKeeper Settings"

    Scores_File_Primary = ConfigSetting("scores.txt")
    Scores_File_Backup1 = ConfigSetting("")
    Scores_File_Backup2 = ConfigSetting("")
# End of class ScoreingSettingsConfig

class sbScoreKeeper(SubSystemConfigBase):
    """Class description:
       Instantiation Syntax: className() See __init__() for syntax details.
    """
    def __init__(self, resetScores: bool = False, redScore: int | None = None, blueScore: int | None = None) -> None:
        """If ResetScores is True and both redScore and blueScore are int()s >= 0 then the scores will be set to the new values.
            Otherwise if ResetScores is false then both redScore and blueScore are ignored."""
        # Be sure to read current score from file after reading the config file.
        if resetScores:
            if isinstance(redScore, int) and isinstance(blueScore, int):
                if redScore >= 0 and blueScore >= 0:
                    self.scoreRed = redScore
                    self.scoreBlue = blueScore
            else:
                if not isinstance(redScore, int) and not isinstance(blueScore, int):
                    raise TypeError("Both redScore and blueScore parameters need to be and instance of int().")
                if not isinstance(redScore, int):
                    raise TypeError("Parameter: redScore needs to be an int().")
                if not isinstance(blueScore, int):
                    raise TypeError("Parameter: blueScore needs to be an int().")
        super().__init__()
        # updateLEDs will be assigned to the appropriate functions/methods during setup. Otherwise they do nothing
        self.updateLEDs = self.dummyMethond
        print(f"Start Executing: sbSounds.__init__() For class: {self.__class__.__qualname__}")
    # End of Method __init__ 

    settings = ScoreingSettingsConfig()

    def incrimentRedScore(self) -> None:
        """"""
        self.scoreRed += 1
        print(f" Red score: {self.scoreRed}")
        self.writeScoresToFile(self.scoreRed, self.scoreBlue)
        self.updateLEDs()
    def incrimentBlueScore(self) -> None:
        """"""
        self.scoreBlue += 1
        print(f"Blue score: {self.scoreBlue}")
        self.writeScoresToFile(self.scoreRed, self.scoreBlue)
        self.updateLEDs()

    def readScoresFromFile(self) -> tuple[int, int]:
        """"""
        with open(self.settings.Scores_File_Primary,'r') as f:
            linesList = f.readlines(1000)
            red = int(linesList[0])
            blue = int(linesList[1])
            return red, blue

    def writeScoresToFile(self, red: int, blue: int) -> None:
        """"""
        with open(self.settings.Scores_File_Primary,'w') as f:
            f.write(f"{red}\n{blue}\n")

    def preSetupPostSettingsUpdateGetExternalData(self):
        """"""
        super().preSetupPostSettingsUpdateGetExternalData()
        # If Both attributes exist and are in int()s >= 0 then reset the score file to these values.
        reset = False
        if hasattr(self, "scoreRed") and hasattr(self, "scoreBlue"):
            if isinstance(self.scoreRed, int) and isinstance(self.scoreBlue, int):
                if self.scoreRed >= 0 and self.scoreBlue >= 0:
                    self.writeScoresToFile(self.scoreRed, self.scoreBlue)
                    reset = True
        if reset:
            (self.scoreRed, self.scoreBlue) = self.readScoresFromFile()
    # End of Method preSetupPostSettingsUpdateGetExternalData 

    def setupSubSys(self) -> None:
        """"""
        # Do common setup actions.
        super().setupSubSys()

    def dummyMethond(self) -> None:
        """dummyMethond is just for initializing references to collable objects"""
        pass
# End of class sbScoreKeeper

# sbScoreKeeperMpSpawning() Loads and Plays the sounds for the Scoreboard.
class sbScoreKeeperMpSpawning(sbScoreKeeper, SpawnProcess):
    """
    sbScoreKeeperMpSpawning() 
    Instantiation Syntax: sbScoreKeeperMpSpawning()
    """

    def __init__(self, resetScores: bool = False, redScore: int | None = None, blueScore: int | None = None) -> None:
        """"""
        print(f"Executing: sbScoreKeeperMpSpawning.__init__()")
        sbScoreKeeper.__init__(self, resetScores, redScore, blueScore)
        SpawnProcess.__init__(self, SCORE_PROCESS_NAME)
        # Setup Score Incriment Queues
        self.queueRedScoreIncriment = self.createQueue()
        self.queueBlueScoreIncriment = self.createQueue()
        # Setup Scores shareing
        self.queueRedScore = self.createQueue()
        self.queueBlueScore = self.createQueue()
        print(f"Done Executing: sbScoreKeeperMpSpawning.__init__()")

    def run_setup(self) -> bool:
        """"""
        print(f'{self.name} process is setting up!', flush=True)
        self.setupSubSys()
        #self.queueRedScore.put(self.scoreRed)
        #self.queueBlueScore.put(self.scoreBlue)

    def run_loop(self) -> bool:
        """run_loop() is called inside run()'s "while True" Loop after checking that the exit event is not set.
            run_loop() returns a True if the default sleep should be used. 
            """
        if not self.queueRedScoreIncriment.empty() or not self.queueBlueScoreIncriment.empty():
            print("Updating scores.")
            # Flushing red queue
            self.scoreRed += self.flushScoreIncrimentQueue(self.queueRedScoreIncriment, "Red")
            self.queueRedScore.put(self.scoreRed)
            # Flushing red queue
            self.scoreBlue += self.flushScoreIncrimentQueue(self.queueBlueScoreIncriment, "Blue")
            self.queueBlueScore.put(self.scoreBlue)
            # Write scores to file.
            self.writeScoresToFile(self.scoreRed, self.scoreBlue)
            print(f"Red: {self.scoreRed}; Blue: {self.scoreBlue}", flush=True)
            return False
        else:
            return True

    def run_shutdownMustRun(self) -> None:
        """"""
        self.shutdownSubSys()

    def flushScoreIncrimentQueue(self, q: QueueType, c: str = "") -> int:
        x = 0
        for i in range(30):
            d = 0
            try:
                d = q.get(True, 0.002)
            except QueueEmptyException:
                break
            finally:
                x += d
            #sleep(0.001)
        print(f"  Incriment {c}{"" if c == "" else " "}score {x} times.", flush=True)
        return x
# End of class sbScoreKeeperMpSpawning

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
    print(f"blue: {buttons.scoreBlue}, red: {buttons.scoreRed}\n")

    # Return 0 is considered a “successful termination”; anyother value is seen as an error by the OS.)
    return 0 
# End of main() Function  

# Call main function if this is the top level Module 
if __name__ == '__main__':
    sys.exit(main()) 