# sbScoreKeeper.py
# 
# Description: 
# 
#

import sys
from time import sleep   # System-specific parameters and functions
#import os    # Miscellaneous operating system interfaces

from .configSetttingsBase import ConfigSettingsBase, ConfigSetting, ConfigSettingBool, SubSystemConfigBase
from .processSpawning import SpawnProcess, SharedInteger32, cast as CastType, QueueType, QueueEmptyException
from .sbButtonsInterface import BUTTONS_PROCESS_NAME, sbButtonsInterfaceMpSpawning

# Define Constents Here
SCORE_KEEPER_PROCESS_NAME = "Score_Keeper"

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
        if not reset:
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
        SpawnProcess.__init__(self, SCORE_KEEPER_PROCESS_NAME)
        # Setup Scores shareing
        #self.queueRedScore = self.createQueue()
        #self.queueBlueScore = self.createQueue()
        self.scoreRedShareing = SharedInteger32(True)
        self.scoreBlueShareing = SharedInteger32(True)
        self._lockScoreFile = self.createLock()
        print(f"Done Executing: sbScoreKeeperMpSpawning.__init__()")
    # End of Method __init__ 

    def readScoresFromFile(self) -> tuple[int, int]:
        """"""
        with self._lockScoreFile:
            values = super().readScoresFromFile()
        return values
    def writeScoresToFile(self, red: int, blue: int) -> None:
        """"""
        with self._lockScoreFile:
            super().writeScoresToFile(red,blue)

    def preStartSetup(self) -> None:
        """preStartSetup() needs to be run before start is called and after the other SpawnProcess instances are initialized.
            Override this to do somethign usefull."""
        self.preSetupPostSettingsUpdateGetExternalData()
        self.scoreRedShareing.value = self.scoreRed
        self.scoreBlueShareing.value = self.scoreBlue
        buttonsProcess = CastType(sbButtonsInterfaceMpSpawning, self.getInstancesByProcessName()[BUTTONS_PROCESS_NAME])
        self.assignQueuesScoreIncrementors(buttonsProcess.queueRedScoreIncriment, buttonsProcess.queueBlueScoreIncriment)
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
        if not hasattr(self, "queueRedScoreIncriment"):
            print(f"{self.name} is not ready to start because: Assignment of queueRedScoreIncriment has not occurred.")
            readyToStart = False
        if not hasattr(self, "queueBlueScoreIncriment"):
            print(f"{self.name} is not ready to start because: Assignment of queueBlueScoreIncriment has not occurred.")
            readyToStart = False
        return readyToStart

    def run_setup(self) -> bool:
        """"""
        print(f"{self.nameAndPID} process is setting up!", flush=True)
        self.setupSubSys()
        #self.queueRedScore.put(self.scoreRed)
        #self.queueBlueScore.put(self.scoreBlue)
        return True

    def run_loop(self) -> bool:
        """run_loop() is called inside run()'s "while True" Loop after checking that the exit event is not set.
            run_loop() returns a True if the default sleep should be used. 
            """
        if not self.queueRedScoreIncriment.empty() or not self.queueBlueScoreIncriment.empty():
            print("Updating scores.")
            # Flushing red queue
            self.scoreRed += self.flushScoreIncrimentQueue(self.queueRedScoreIncriment, "Red")
            self.scoreRedShareing.value = self.scoreRed
            #self.queueRedScore.put(self.scoreRed)
            # Flushing red queue
            self.scoreBlue += self.flushScoreIncrimentQueue(self.queueBlueScoreIncriment, "Blue")
            self.scoreBlueShareing.value = self.scoreBlue
            #self.queueBlueScore.put(self.scoreBlue)
            # Write scores to file.
            self.writeScoresToFile(self.scoreRed, self.scoreBlue)
            print(f"Red: {self.scoreRed}; Blue: {self.scoreBlue}", flush=True)
            return False
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
        print(f"  Incriment {c}{'' if c == "" else ''}score {x} times.", flush=True)
        return x

    def assignQueuesScoreIncrementors(self, redQueue, blueQueue) -> None:
        """"""
        self.queueRedScoreIncriment = self.assignQueue(redQueue)
        self.queueBlueScoreIncriment = self.assignQueue(blueQueue)
        self.run_setup
# End of class sbScoreKeeperMpSpawning

# -----------------------------------------------------------------------------

# Define the "Main" Function. If this is not the program module this function can be used for isolated debug testing by executing this file.
def main() -> int:
    """This is the "Main" function which is called automatically by the last two lines if this is the top level Module. 'Import this_file' will not call main().
    """
    from .processSpawning import setStartMethod, allSpawnedProcesses_preStartSetup, allSpawnedProcesses_isReadyToStart, SpawnedProcess_getEventExitAllProcesses
    from .processSpawning import allSpawnedProcesses_start, allSpawnedProcesses_ShutdownAndClose
    import argparse
    pCmdLine = argparse.ArgumentParser()
    pCmdLine.add_argument("-rs", "--resetScores", action="store_True", help="Reset args to red & blue values specified on command line.")
    pCmdLine.add_argument("-s", "--scores", type=int, nargs=2, help="Set Red & Blue scores. Useage: '-s 3 14' for red=3 & blue=14")
    pCmdLine.add_argument("-r", "--redScore", type=int, help="Set Red score. Useage: '-r 3' for red=3")
    pCmdLine.add_argument("-b", "--blueScore", type=int, help="Set Blue score. Useage: '-r 14' for blue=14")
    args = pCmdLine.parse_args()

    # Import Local modules here.
    from sbSounds import sbSoundsMpSpawning
    from sbScoreKeeper import sbScoreKeeperMpSpawning
    from sbDotStarLEDs import sbDotStarLEDsMpSpawning
    print("Main: Done Importing loc modules.")

    buttons = sbButtonsInterfaceMpSpawning()
    if args.resetScores:
        if isinstance(args.scores, list) and len(args.scores) == 2 and args.scores[0] >= 0 and args.scores[1] >= 0:
            scoreKeep = sbScoreKeeperMpSpawning(True, args.scores[0], args.scores[1])
        elif isinstance(args.red, int) and isinstance(args.blue, int) and args.red >= 0 and args.blue >= 0:
            scoreKeep = sbScoreKeeperMpSpawning(True, args.red, args.blue)
        else:
           scoreKeep = sbScoreKeeperMpSpawning()
    else:
        scoreKeep = sbScoreKeeperMpSpawning()
    sounds = sbSoundsMpSpawning()
    dotstar = sbDotStarLEDsMpSpawning()
    isExitEventSet = SpawnedProcess_getEventExitAllProcesses().is_set
    print(f"{isExitEventSet()} = Exit All Processes event from Main.")
    print("Main: Done initializing subsystem classes.")

    print(f"Main: Calling Pre start setup for all Process(es).")
    allSpawnedProcesses_preStartSetup()
    notReady = allSpawnedProcesses_isReadyToStart()
    if len(notReady) > 0:
        print(f"These modules are not ready to start: {notReady}")
        allSpawnedProcesses_ShutdownAndClose()
        return 1

    # Setup Done now start processes
    allSpawnedProcesses_start()

    # wait on user input or exit All event to be set
    while True:
        try:
            if isExitEventSet():
                print("Exit event was detected so exiting.")
                break
            # Run until someone presses enter or types exit or quit.
            inp = input("To exit Press enter or type exit or quit. For Scores: sr, sb. For Effects: re, be.\n")
            match inp.lower():
                case "":
                    print("Enter was pressed so exiting.")
                    break
                case "exit" | "quit":
                    print(f"Exiting because '{inp}' was typed.")
                    break
                case "sr":
                    print(f"Triggering Score Red because '{inp}' was typed.")
                    buttons.scoreRedCallBack()
                case "sb":
                    print(f"Triggering Score Blue because '{inp}' was typed.")
                    buttons.scoreBlueCallBack()
                case "re":
                    print(f"Triggering Red Effects because '{inp}' was typed.")
                    buttons.effectRedCallBack()
                case "be":
                    print(f"Triggering Blue Effects because '{inp}' was typed.")
                    buttons.effectBlueCallBack()
        finally:
            # Clean up
            allSpawnedProcesses_ShutdownAndClose()

    # Return 0 is considered a “successful termination”; anyother value is seen as an error by the OS.)
    return 0 
# End of main() Function  

# Call main function if this is the top level Module 
if __name__ == '__main__':
    sys.exit(main()) 