# processSpawning.py
# 
# Description: 
# 
#

import sys   # System-specific parameters and functions
#import os    # Miscellaneous operating system interfaces
import multiprocessing

# Define Functions and Classes Here
class SpawnProcess(multiprocessing.Process):
    """Class description:
       Instantiation Syntax: className() See __init__() for syntax details.
    """
    exitAll = None
    def __init__(self, pName = None) -> None:
        """Customize the current instance to a specific initial state."""
        super().__init__(name = pName)
    
    def run(self) -> None:
        """"""
        # TODO: Call Setup method here
        while True:
            # TODO: Call Loop Method here
            if True: # TODO: Make Shutdown event
                break
# End of class className
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