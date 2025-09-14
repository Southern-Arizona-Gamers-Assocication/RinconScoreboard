# processSpawning.py
# 
# Description: 
# 
# 

from concurrent.futures import ThreadPoolExecutor
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
    __instancesByProcessName: dict[str, mp.Process] = {} # TODO make this a readonly descriptor.
    @classmethod
    def getInstancesByProcessName(cls):
        """"""
        return cls.__instancesByProcessName

    __processNames: list[str] = []      # TODO make this a readonly descriptor.
    @classmethod
    def getProcessNames(cls):
        """"""
        return cls.__processNames

    __processNamesCount = Counter()     # TODO make this a readonly descriptor.
    @classmethod
    def getProcessNamesCount(cls):
        """"""
        return cls.__processNamesCount

    __exitAllProcesses = mp.Event()
    @classmethod
    def getEventExitAllProcesses(cls):
        """The first time this is run, create one Exit event to exit the run()'s "while True" loop. 
            This event needs to be shared by all instances of this class and subclasses so all the 
            processes end and be joined gracefully. """
        return cls.__exitAllProcesses
    eventType = type(__exitAllProcesses)
    
    def __init__(self, pName: str = "", ) -> None:
        """Customize the current instance to a specific initial state."""
        #print(f"Start Executing: SpawnProcess.__init__()")
        # On first call create the exitAllProcesses event, all other times do nothing because the event is already created. 
        if len(self.__processNames) < 1:
            self.__class__.__exitAllProcesses = mp.Event()
        self.__exitAllProcesses = self.assignEvent(self.__class__.__exitAllProcesses)
        # settign the processes name and making is unique.
        if not (isinstance(pName, str) and len(pName) > 0):
            pName = self.__class__.__name__
        self.__processNamesCount.update([pName])
        i = self.__processNamesCount[pName]
        if i > 1:
            pName = f"{pName}-{i}"
        # Log the this classes instances and Process names
        self.__instancesByProcessName[pName] = self
        self.__processNames.append(pName)
        super().__init__(name = pName)
        self.nameAndPID = f"PID={self.pid}: {self.name}"
        # Create the Setup Done instance
        self.setupDone = self.createEvent()
        self.__startHasNotRun = True    # TODO make this a readonly descriptor.
        print(f"{self.__exitAllProcesses} = Exit All Processes event from {pName}.")
        #print(f"{pName} is done Executing: SpawnProcess.__init__()")

    def didStartRun(self) -> bool:
        """didStartRun() returns True if Start was successfully executed."""
        return not self.__startHasNotRun

    def start(self):
        """Start the process's activity after passing a check to see if this instance is ready to start 
            (method readyToStart() returns true). If readyToStart() returns false, a RuntimeError is raised. 
            This must be called at most once per process object. It arranges for the object's run() method 
            to be invoked in a separate process."""
        if self.__startHasNotRun:
            if self.isReadyToStart():
                # Actually calling Process.start(). Now this can't be done again in the same instance.
                self.__startHasNotRun = False
                super().start()
                print(f"{self.nameAndPID} is done calling start()", flush=True)
            else:
                raise RuntimeError(f"{self.nameAndPID}.isReadyToStart() returned False so this process is not " +
                                    "ready to start. Check the logic in isReadyToStart() and it's subclass overrides.")
        else:
            raise RuntimeError(f"{self.nameAndPID}: Start has called more than once ")

    def run(self) -> None:
        """IF Overriding this Method, the main loop should not be replaced but more complex Setup and Shutdown can be used. 
            This method NEEDS to be called to keep most functionality. Ex: super().run() """
        try:
            self.nameAndPID = f"{self.name}(PID: {self.pid})"
            self.run_setup()
            self.setupDone.set()
            while True:
                if  self.__exitAllProcesses.is_set():
                    print(f'{self.nameAndPID} process noticed that the event exitAllProcesses is set! Now exiting.', flush=True)
                    break
                if self.run_loop():
                    sleep(0.1)
            self.run_shutdown()
        finally:
            self.__exitAllProcesses.set()
            self.run_shutdownMustRun()

    def isReadyToStart(self) -> bool:
        """IF Overriding this Method, THis one NEEDS to be called. Ex 'super().isReadyToStart()'."""
        if self.didStartRun():
            print(f"{self.nameAndPID}: This instance's start() has already successfully been excicuted.", flush=True)
            return False
        return True
    
    def run_setup(self) -> None:
        """run_setup() is called when run() is starting before the "while True" Loop.
            Override this to do somethign usefull."""
        print(f'{self.nameAndPID} process is setting up!', flush=True)

    def run_loop(self) -> bool:
        """run_loop() is called inside run()'s "while True" Loop after the exit event is checked.
            run_loop() returns a True if the default sleep should be used. 
            Override this to do somethign usefull."""
        print(f'{self.nameAndPID} process running...', flush=True)
        sleep(0.9)
        return True

    def run_shutdown(self) -> None:
        """run_shutdown() is called when run()'s "while True" loop exits normally (ex: a break statement).
            Override this to do somethign usefull."""
        print(f'{self.nameAndPID} process is shutting down!', flush=True)

    def run_shutdownMustRun(self) -> None:
        """run_shutdownMustRun() is called in run()'s try:finally statement so it is always executed.
            This method should only have important resource freeing expressions. 
            Override this to do somethign usefull."""
        pass

    def createQueue(self):
        """"""
        q = mp.Queue(20)
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

    def cleanUpProcess(self) -> None:
        """IF Overriding this Method, THis one NEEDS to be called. Ex 'super().CloseThisProcess()'."""
        if hasattr(self, "queuesList"):
            for q in self.queuesList:
                q.cancel_join_thread()
                q.close()
# End of class SpawnProcess

def shutdownAndCloseOneSpawnedProcess(p: SpawnProcess, pName: str = "") -> tuple[str, int | None]:
    """"""
    if pName == "" or not isinstance(pName, str):
        pName = p.name
    if p.getEventExitAllProcesses().is_set():
        print(f"{pName}.exitAllProcesses.is_set() return true.")
    else:
        p.getEventExitAllProcesses().set()
        print(f"Even exitAllProcesses has been set for process {pName}.")
    # Wait for the process to terminate on its own.
    p.join(5)
    # if the process is still alive (p.join() timedout) then send a terminate signall.
    if p.is_alive():
        print(f"Main: {p.name} Seams to still be running. Sending SIGTERM.")
        p.terminate()
    p.join(1)
    p.cleanUpProcess()
    p.join(3)
    # if the process is still alive (p.join() timedout) then send a kill signall.
    if p.is_alive():
        print(f"Main: {p.name} Seams to still be running. Sending SIGKILL.")
        p.kill()
    p.join(1)
    exitCode = p.exitcode
    print(f"Main is closing the child processes, {pName}.")
    p.close()
    return pName, exitCode

def shutdownAndCloseAllSpawnedProcesses(printResults: bool = False) -> list[tuple[str, int | None]]:
    """"""
    SpawnProcess.getEventExitAllProcesses().set()
    print(f"Main: exitAllProcesses.is_set() returns {SpawnProcess.getEventExitAllProcesses().is_set()}.")
    with ThreadPoolExecutor(max_workers=len(SpawnProcess.getInstancesByProcessName())) as ex:
        results = ex.map(shutdownAndCloseOneSpawnedProcess, 
                         SpawnProcess.getInstancesByProcessName().values(),
                         timeout=60.0)
    resultsList = [r for r in results]
    if printResults:
        for r in resultsList:
            print(f"{r[0]}.exitcode is {r[1]}")
    return resultsList
# -----------------------------------------------------------------------------

class DeltaProcess(SpawnProcess):
    __exitAllProcesses = "Not correct"
class EpsilonProcess(SpawnProcess):
    __processNamesCount = "Not correct"

# Define the "Main" Function. If this is not the program module this function can be used for isolated debug testing by executing this file.
def main() -> int:
    """This is the "Main" function which is called automatically by the last two lines if this is the top level Module. 'Import this_file' will not call main().
    """
    print(f"The Global Start Method is '{mp.get_start_method(allow_none=True)}' ")
    mp.set_start_method('spawn', True)
    print(f"The Global Start Method is '{mp.get_start_method(allow_none=True)}' ")
    
    processes = [SpawnProcess(s) for s in ["Alpha"]*5 + ["Beta"]*4 + ["Gamma"]*3]
    processes.append(DeltaProcess())
    processes += [EpsilonProcess(s) for s in [""]*2]

    print(f"{SpawnProcess.getEventExitAllProcesses()} = Exit All Processes event from Main.")
    print(f"Main: exitAllProcesses.is_set() returns {SpawnProcess.getEventExitAllProcesses().is_set()}.")

    print(f"Main: Starting {len(processes)} Child Process(es).")
    for p in processes:
        p.start()

    print("Main is going to sleep for 4 seconds.")
    sleep(4)
    
    print("Main: Time to shutdown.")
    shutdownAndCloseAllSpawnedProcesses(True)

    # Return 0 is considered a “successful termination”; anyother value is seen as an error by the OS.)
    return 0 
# End of main() Function  

# Call main function if this is the top level Module 
if __name__ == '__main__':
    #mp.set_start_method('spawn')
    sys.exit(main()) 