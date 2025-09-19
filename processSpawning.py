# processSpawning.py
# 
# Description: 
# 
# 
#from __future__ import annotations

import sys   # System-specific parameters and functions
import os    # Miscellaneous operating system interfaces
from collections import Counter
from time import sleep
from typing import Final, final, cast
import multiprocessing as mp
from multiprocessing.synchronize import Event as EventType
from multiprocessing.queues import Queue as QueueType
from queue import Empty as QueueEmptyException, Full as QueueFullException
from multiprocessing.shared_memory import SharedMemory
from concurrent.futures import ThreadPoolExecutor

# Define Functions and Classes Here
class SharedInteger32:
    """creates a shared memory location for multiple processes to share an integer. """
    __maxbits = 32
    __maxBytes = (__maxbits//8) + (__maxbits%8 > 0)
    __maxValue = 2**(__maxbits-1)-1
    __minValue = -2**(__maxbits-1)
    __byteOrder = sys.byteorder
    def __init__(self, shareName: str|None = None, value: int|None = None) -> None:
        """
        __init__() Initialise the class and creates or attaches to a shared memory locaton for a 32 bit signed integer (-2^31 to 2^31 -1).

        :param shareName: The name of the shared space. If sharedName is "" or None create the shared memory space otherwise attach to an exiting one.
        :type shareName: str | None
        :param value: The int to share if createing a the shared memory space. If attaching to an existing share, "value" is ignored. 
        :type value: int
        """
        if shareName == "" or shareName == None:
            self.name = None
            createSM = True
        elif isinstance(value, str):
            self.name = shareName
            createSM = False
        else:
            raise TypeError("Parameter, 'shareName', needs to be of type str or None.")
        if isinstance(value, int):
            self.__value = value
        else:
            raise TypeError("Parameter, 'value', needs to be of type int.")
        self.__MemoryToShare = SharedMemory(shareName, createSM, self.__maxBytes)
        self.__name = self.__MemoryToShare.name
        self.__memBuf = self.__MemoryToShare.buf
        if createSM:
            self.__memBuf = value.to_bytes(self.__maxBytes)
        self.__lock = mp.Lock()
        

    def int32FromBytes(self, byteArray) -> int:
        """"""
        return int(0)
    def __get__(self, instance, owningClass=None):
        """"""
        return int.from_bytes(self.__memBuf)
    
    def __set__(self, instance, value: int):
        """"""
        pass
        #raise AttributeError(f"{self.__nameMe__} is a READ ONLY attribute. Use class (or a subclass of) ConfigSettingsBase's update* Methods.")
# End of class SharedInteger

class SpawnProcess(mp.Process):
    """Class description:
       Instantiation Syntax: className() See __init__() for syntax details.
    """
    DEFAULT_QUEUE_SIZE = 30
    __instancesByProcessName: Final[dict[str, "SpawnProcess"]] = {} # TODO make this a readonly descriptor.
    @classmethod
    @final
    def getInstancesByProcessName(cls):
        """"""
        return cls.__instancesByProcessName

    __processNames: Final[list[str]] = []      # TODO make this a readonly descriptor.
    @classmethod
    @final
    def getProcessNames(cls):
        """"""
        return cls.__processNames

    __processNamesCount: Final[Counter[str]] = Counter()     # TODO make this a readonly descriptor.
    @classmethod
    @final
    def getProcessNamesCount(cls):
        """"""
        return cls.__processNamesCount

    #__exitAllProcesses: Event = None # pyright: ignore[reportAssignmentType]
    @classmethod
    @final
    def getEventExitAllProcesses(cls) -> EventType:
        """The first time this is run, create one Exit event to exit the run()'s "while True" loop. 
            This event needs to be shared by all instances of this class and subclasses so all the 
            processes end and be joined gracefully. """
        return cls.__exitAllProcesses
    
    def __init__(self, pName: str = "", ) -> None:
        """Customize the current instance to a specific initial state."""
        #print(f"Start Executing: SpawnProcess.__init__()")
        # On first call create the exitAllProcesses event. 
        if len(self.__processNames) < 1:
            SpawnProcess.__exitAllProcesses: Final[EventType] = self.createEvent() # try changing to: SpawnProcess.__exitAllProcesses: Final[Event]
        # Set the instance.exitAllProcesses to the base class level SpawnProcess.exitAllProcesses event. 
        self.exitAllProcesses: Final[EventType] = self.assignEvent(self.getEventExitAllProcesses())
        # settign the processes name and making is unique.
        if not (isinstance(pName, str) and len(pName) > 0):
            pName = self.__class__.__name__
        self.getProcessNamesCount().update([pName])
        i = self.getProcessNamesCount()[pName]
        if i > 1:
            pName = f"{pName}-{i}"
        # Log the this classes instances and Process names
        self.getInstancesByProcessName()[pName] = self
        self.getProcessNames().append(pName)
        super().__init__(name = pName)
        self.nameAndPID = f"PID={self.pid}: {self.name}"
        # Create the Run Progress Events for this instance.
        self.__startHasRun: Final[EventType] = self.createEvent()
        self.__setupDone: Final[EventType] = self.createEvent()
        self.__shutdownMustRunCalled: Final[EventType] = self.createEvent()
        print(f"PID: {os.getpid()}; ) {pName}. ")
        #print(f"{pName} is done Executing: SpawnProcess.__init__()")
    # End of method __init__

    def preStartSetup(self) -> None:
        """preStartSetup() needs to be run before start is called and after the other SpawnProcess instances are initialized.
            Override this to do somethign usefull."""
        #print(f'{self.name} process is done with pre Start setup.')
        pass

    @final
    def start(self):
        """Start the process's activity after passing a check to see if this instance is ready to start 
            (method readyToStart() returns true). If readyToStart() returns false, a RuntimeError is raised. 
            This must be called at most once per process object. It arranges for the object's run() method 
            to be invoked in a separate process."""
        if self.__startHasRun.is_set():
            raise RuntimeError(f"{self.name}: Start has called more than once ")
        else:
            if self.isReadyToStart():
                # Actually calling Process.start(). Now this can't be done again in the same instance.
                super().start()
                self.__startHasRun.set()
                print(f"{self.name} is done calling start()", flush=True)
            else:
                raise RuntimeError(f"{self.name}.isReadyToStart() returned False so this process is not " +
                                    "ready to start. Check the logic in isReadyToStart() and it's subclass overrides.")

    def run(self) -> None:
        """IF Overriding this Method, the main loop should not be replaced but more complex Setup and Shutdown can be used. 
            This method NEEDS to be called to keep most functionality. Ex: super().run() """
        try:
            self.nameAndPID = f"PID={self.pid}: {self.name}"
            useLoop = self.run_setup()
            self.__setupDone.set()
            if useLoop:
                while True:
                    if  self.exitAllProcesses.is_set():
                        print(f'{self.nameAndPID} process noticed that the event exitAllProcesses is set! Now exiting.', flush=True)
                        break
                    if self.run_loop():
                        sleep(0.1)
            else:
                self.exitAllProcesses.wait()
            self.run_shutdown()
        finally:
            self.exitAllProcesses.set()
            self.run_shutdownMustRun()
            self.__shutdownMustRunCalled.set()

    def isReadyToStart(self) -> bool:
        """IF Overriding, this Method NEEDS to be called. Ex 'super().isReadyToStart()'."""
        if self.__startHasRun.is_set():
            print(f"{self.nameAndPID}: This instance's start() has already successfully been excicuted.", flush=True)
            return False
        return True
    
    def run_setup(self) -> bool:
        """run_setup() is called when run() is starting before the "while True" Loop.
            run_setup() returns True to call run_loop() from the "while True" Loop or False to block while waiting for the exit all events to be set. 
            Override this to do somethign usefull."""
        print(f"(Parent's PID: {os.getppid()}){self.nameAndPID} process is done setting up!", flush=True)
        return True

    def run_loop(self) -> bool:
        """run_loop() is called inside run()'s "while True" Loop after checking that the exit event is not set.
            run_loop() returns a True if the default sleep should be used. 
            Override this to do somethign usefull."""
        sleep(0.9)
        return True

    def run_shutdown(self) -> None:
        """run_shutdown() is called when run()'s "while True" loop exits normally (ex: a break statement).
            Override this to do somethign usefull."""
        print(f"{self.nameAndPID} process is shutting down!", flush=True)

    def run_shutdownMustRun(self) -> None:
        """run_shutdownMustRun() is called in run()'s try:finally statement so it is always executed.
            This method should only have important resource freeing expressions. 
            Override this to do somethign usefull."""
        pass

    @final
    def didStartRun(self) -> bool:
        """didStartRun() returns True if Start was successfully executed."""
        return self.__startHasRun.is_set()
    @final
    def isSetupDone(self) -> bool:
        """didStartRun() returns True if Start was successfully executed."""
        return self.__setupDone.is_set()
    @final
    def wasShutdownMustRunCalled(self) -> bool:
        """didStartRun() returns True if Start was successfully executed."""
        return self.__shutdownMustRunCalled.is_set()

    def createEvent(self) -> EventType:
        """"""
        return mp.Event()
    def assignEvent(self, e: EventType) -> EventType:
        """"""
        if not isinstance(e, EventType):
            raise ValueError("The event parameter must ultimately be assigned by multiprocessing.Event() or None if it is to be assigned later. " + 
                             "It must be assigned before calling .start(). Calling assignEvent() is the easiest method.")
        return e

    def createQueue(self, size: int = DEFAULT_QUEUE_SIZE) -> QueueType:
        """"""
        q = mp.Queue(size)
        if hasattr(self, "queuesList"):
            self.queuesList.append(q)
        else:
            self.queuesList: list[QueueType] = [q]
        return q
    def assignQueue(self, q: QueueType) -> QueueType:
        """"""
        if not isinstance(q, QueueType):
            raise ValueError("The queue parameter must ultimately be assigned by multiprocessing.Queue() or None if it is to be assigned later. " + 
                             "It must be assigned before calling .start(). Calling assignQueue(.createQueue()) is the easiest method.")
        return q

    def cleanUpProcess(self) -> None:
        """IF Overriding this Method, THis one NEEDS to be called. Ex 'super().CloseThisProcess()'."""
        if self.__startHasRun.is_set() and not self.__shutdownMustRunCalled.is_set():
            print(f"{self.name}.run_shutdownMustRun() is running at cleanup ")
            self.run_shutdownMustRun()
            self.__shutdownMustRunCalled.set()
        if hasattr(self, "queuesList"):
            for q in self.queuesList:
                q.cancel_join_thread()
                q.close()
# End of class SpawnProcess

def SpawnedProcessShutdownAndClose(p: SpawnProcess, pName: str = "") -> tuple[str, int | None]:
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
# End of function shutdownAndCloseOneSpawnedProcess

def shutdownAndCloseAllSpawnedProcesses(printResults: bool = False) -> list[tuple[str, int | None]]:
    """"""
    SpawnProcess.getEventExitAllProcesses().set()
    print(f"Main: exitAllProcesses.is_set() returns {SpawnProcess.getEventExitAllProcesses().is_set()}.")
    with ThreadPoolExecutor(max_workers=len(SpawnProcess.getInstancesByProcessName())) as ex:
        results = ex.map(SpawnedProcessShutdownAndClose, 
                         SpawnProcess.getInstancesByProcessName().values(),
                         timeout=60.0)
    resultsList = [r for r in results]
    if printResults:
        for r in resultsList:
            print(f"{r[0]}.exitcode is {r[1]}")
    return resultsList
# End of function shutdownAndCloseAllSpawnedProcesses

# -----------------------------------------------------------------------------

# Define the "Main" Function. If this is not the program module this function can be used for isolated debug testing by executing this file.
def main() -> int:
    """This is the "Main" function which is called automatically by the last two lines if this is the top level Module. 'Import this_file' will not call main().
    """
    print(f"The Global Start Method is '{mp.get_start_method(allow_none=True)}' ")
    mp.set_start_method('spawn', True)
    print(f"The Global Start Method is '{mp.get_start_method(allow_none=True)}' ")
    
    processes = [SpawnProcess(s) for s in ["Alpha"]*6 + ["Beta"]*3 + ["Gamma"]*4]

    print(f"{SpawnProcess.getEventExitAllProcesses()} = Exit All Processes event from Main.")
    print(f"Main: exitAllProcesses.is_set() returns {SpawnProcess.getEventExitAllProcesses().is_set()}.")

    print(f"Main: Calling Pre start setup for all Process(es).")
    for p in processes:
        p.preStartSetup()

    print(f"Main: Starting {len(processes)} Child Process(es).")
    for p in processes:
        p.start()
    #sleep(2)

    print("Main is waiting for the Stop Event for a max of 5 seconds.")
    SpawnProcess.getEventExitAllProcesses().wait(5)
    
    print("Main: Time to shutdown.")
    shutdownAndCloseAllSpawnedProcesses(True)

    # Return 0 is considered a “successful termination”; anyother value is seen as an error by the OS.)
    return 0 
# End of main() Function  

# Call main function if this is the top level Module 
if __name__ == '__main__':
    #mp.set_start_method('spawn')
    sys.exit(main()) 