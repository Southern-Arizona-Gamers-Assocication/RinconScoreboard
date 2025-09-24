# scoreboard.py

import sys
#import os

from time import sleep

if sys.prefix != "/home/pi/Code/RinconScoreboard/venv":
    raise OSError("This file must be run in a virtual environment (venv). To start venv, from the project directory type:\n" \
                    "source venv/bin/activate")

# Import Local modules here.
print("Main: Start importing subsystem modules.")
from sbButtonsInterface import sbButtonsInterfaceMpSpawning
from sbScoreKeeper import sbScoreKeeperMpSpawning
from sbSounds import sbSoundsMpSpawning
from sbDotStarLEDs import sbDotStarLEDsMpSpawning
print("Main: Done importing subsystem modules.")

# Still need FTDI drivers 
# from ftdi.dmx_controller.OpenDmxUsb import OpenDmxUsb

# -----------------------------------------------------------------------------

# Define the "Main Function" which is called automatically if this is the top level Module by the last two lines 
def main() -> int:
    """This is the "Main" function which is called automatically by the last two lines if this is the top level Module. 'Import this_file' will not call main().
    """
    from processSpawning import allSpawnedProcesses_preStartSetup, allSpawnedProcesses_isReadyToStart, allSpawnedProcesses_start
    from processSpawning import setStartMethod, SpawnedProcess_getEventExitAllProcesses, allSpawnedProcesses_ShutdownAndClose
    setStartMethod()

    import argparse
    pCmdLine = argparse.ArgumentParser()
    pCmdLine.add_argument("-rs", "--resetScores", action="store_true", help="Reset args to red & blue values specified on command line.")
    pCmdLine.add_argument("-s", "--scores", type=int, nargs=2, help="Set Red & Blue scores. Useage: '-s 3 14' for red=3 & blue=14")
    pCmdLine.add_argument("-r", "--redScore", type=int, help="Set Red score. Useage: '-r 3' for red=3")
    pCmdLine.add_argument("-b", "--blueScore", type=int, help="Set Blue score. Useage: '-r 14' for blue=14")
    args = pCmdLine.parse_args()


    buttons = sbButtonsInterfaceMpSpawning()
    if args.resetScores:
        if isinstance(args.scores, list) and len(args.scores) == 2 and args.scores[0] >= 0 and args.scores[1] >= 0:
            scoreKeep = sbScoreKeeperMpSpawning(True, args.scores[0], args.scores[1])
        elif isinstance(args.redScore, int) and isinstance(args.blueScore, int) and args.redScore >= 0 and args.blueScore >= 0:
            scoreKeep = sbScoreKeeperMpSpawning(True, args.redScore, args.blueScore)
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
        print(f"These subsystems are not ready to start: {notReady}")
        allSpawnedProcesses_ShutdownAndClose()
        return 1

    # Setup Done now start processes
    print(f"Main: Setup Done now start processes")
    allSpawnedProcesses_start()

    # wait on user input or exit All event to be set
    try:
        while True:
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
                case _:
                    print("Unknown Command ")
    finally:
        # Clean up
        allSpawnedProcesses_ShutdownAndClose()

    # End Main Function and Return 0 
    # 0 is considered a “successful termination”; anyother value is seen as an error by the OS.)
    return 0 

# Call main function if this is the top level Module 
if __name__ == '__main__':
    sys.exit(main())  
