# processSpawning.py
# 
# Description: 
# 
# 

import sys   # System-specific parameters and functions
#import os    # Miscellaneous operating system interfaces
from collections import Counter
from time import sleep
from typing import cast
import multiprocessing as mp

# Define Functions and Classes Here
class SpawnProcess(mp.Process):
    """Class description:
       Instantiation Syntax: className() See __init__() for syntax details.
    """
    _instancesByProcessName: dict[str, mp.Process] = {}
    _processNames: list[str] = []
    _processNamesCount = Counter()
    exitAllProcesses = mp.Event()
    eventType = type(exitAllProcesses)

    def __init__(self, pName: str = "", ) -> None:
        """Customize the current instance to a specific initial state."""
        # On first run Set Exit All Processes to be the same.  
        print(f"Start Executing: SpawnProcess.__init__()")
        if len(self._instancesByProcessName) == 0:
            print(f"Setting Creating Event in {pName} process.")
            self.exitAllProcesses = mp.Event()
        if not (isinstance(pName, str) and len(pName) > 0):
            pName = self.__class__.__name__
        self._processNamesCount.update([pName])
        i = self._processNamesCount[pName]
        if i > 1:
            pName = f"{pName}-{i}"
        self._instancesByProcessName[pName] = self
        self._processNames.append(pName)
        super().__init__(name = pName)
        print(f"{pName}'s process names {self._processNamesCount}; event: {self.exitAllProcesses}")
        print(f"Done Executing: SpawnProcess.__init__()")

    def run(self) -> None:
        """IF Overriding this Method, the main loop should not be replaced but more complex Setup and Shutdown can be used. This method NEEDS to be called. Ex: supper().run() """
        try:
            self.run_setup()
            while True:
                self.run_loop()
                if  self.exitAllProcesses.is_set():
                    print(f'{self.name} process noticed that the event exitAllProcesses is set! Now exiting.', flush=True)
                    break
                sleep(0.1)
            self.run_shutdown()
        finally:
            self.exitAllProcesses.set()

    def run_setup(self) -> None:
        """Override this to do somethign usefull."""
        print(f'{self.name} process is setting up!', flush=True)

    def run_loop(self) -> None:
        """Override this to do somethign usefull."""
        print(f'{self.name} process running...', flush=True)
        sleep(0.75)

    def run_shutdown(self) -> None:
        """Override this to do somethign usefull."""
        print(f'{self.name} process is shutting down!', flush=True)

    def createQueue(self):
        """"""
        q = mp.Queue(10)
        if not hasattr(self, "queueType"):
            self.queueType = type(q)
            self.queuesList.append(q)
        else:
            self.queuesList = [q]
        return q

    def createEvent(self):
        """"""
        return mp.Event()
    
    def assignEvent(self, e):
        """"""
        if not isinstance(e, self.eventType):
            raise ValueError("The event parameter must ultimately be assigned by multiprocessing.Event() or None if it is to be assigned later. " + 
                             "It must be assigned before calling .start(). Calling assignEvent() is the easiest method.")
        return e

    def assignQueue(self, q):
        """"""
        if not isinstance(q, self.queueType):
            raise ValueError("The queue parameter must ultimately be assigned by multiprocessing.Queue() or None if it is to be assigned later. " + 
                             "It must be assigned before calling .start(). Calling assignQueue(.createQueue()) is the easiest method.")
        return q

    def CloseThisProcess(self) -> None:
        """IF Overriding this Method, THis one NEEDS to be called. Ex 'supper().CloseThisProcess()'."""
        if hasattr(self, "queuesList"):
            for q in self.queuesList:
                q.cancel_join_thread()
                q.close()

# End of class SpawnProcess

# -----------------------------------------------------------------------------

# Define the "Main" Function. If this is not the program module this function can be used for isolated debug testing by executing this file.
def main() -> int:
    """This is the "Main" function which is called automatically by the last two lines if this is the top level Module. 'Import this_file' will not call main().
    """
    print(f"The Global Start Method is '{mp.get_start_method(allow_none=True)}' ")
    mp.set_start_method('spawn', True)
    print(f"The Global Start Method is '{mp.get_start_method(allow_none=True)}' ")
    
    exitEvent = mp.Event()
    p1 = SpawnProcess("Alpha")
    p2 = SpawnProcess("Beta")

    print("Main: Starting Child Processes")
    p1.start()
    p2.start()

    print("Main is going to sleep for 3 seconds.")
    sleep(4)

    print("Main:  exitAllProcesses is being set.")
    p1.exitAllProcesses.set()
    print(f"Main: exitAllProcesses.is_set() returns {p2.exitAllProcesses.is_set()}.")

    p1.join(5)
    p2.join(5)

    if p1.is_alive():
        print(f"Main: {p1.name} Seams to still be running. Sending SIGTERM.")
        p1.terminate()
    if p2.is_alive():
        print(f"Main: {p2.name} Seams to still be running. Sending SIGTERM.")
        p2.terminate()

    p1.join(5)
    p2.join(5)

    if p1.is_alive():
        print(f"Main: {p1.name} Seams to still be running. Sending SIGKILL.")
        p1.kill()
    if p2.is_alive():
        print(f"Main: {p2.name} Seams to still be running. Sending SIGKILL.")
        p2.kill()

    p1.join(2)
    p2.join(2)

    print("Main is closing the child processes.")
    p1.close()
    p2.close()

    # Return 0 is considered a “successful termination”; anyother value is seen as an error by the OS.)
    return 0 
# End of main() Function  

# Call main function if this is the top level Module 
if __name__ == '__main__':
    #mp.set_start_method('spawn')
    sys.exit(main()) 