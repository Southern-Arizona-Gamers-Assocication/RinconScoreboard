# configFileParser.py
# 
# Description: 
# 
#

import sys   # System-specific parameters and functions
import os    # Miscellaneous operating system interfaces
from configparser import ConfigParser

from configSetttingsBase import ConfigSettingsBase
import configSetttingsBase

# Define Functions and Classes Here

class configFileParser:
    """Class description:
       Instantiation Syntax: className() See __init__() for syntax details.
    """
    def __init__(self, configFileName: str):
        """
        __init__() sets the initial state of the class instance. If fileName is None then no.

        :param configFileName: The name of the file to load.
        :type configFileName: str
        """
        self.__configFileName__ = configFileName
        self.configSections: dict[str, ConfigSettingsBase] = {}
        self.config = ConfigParser()
    
    def registerSettingsSection(self, sectionSettings: ConfigSettingsBase):
        """
        registerSettingsSection Registers a setting section and loads the settings into the ConfigParcser

        :param Settings: The settings from the class ConfigSettingsBase or one of its Subclasses. 
        :type Settings: ConfigSettingsBase
        """
        if not isinstance(sectionSettings, ConfigSettingsBase):
            raise TypeError(f"Error with registeringSettingsSection argument of type {type(sectionSettings)}. The type should be 'class ConfigSettingsBase'")
        sectionName = sectionSettings.sectionName()
        self.configSections[sectionName] = sectionSettings
        self.loadSectonIntoConfig(sectionName)

    def loadSectonIntoConfig(self, sectionName: str):
        """"""
        self.config[sectionName] = self.configSections[sectionName].getAllSectionSettings()

    def loadAllSectonsIntoConfig(self):
        """"""
        for sectionName in self.configSections.keys():
            self.config[sectionName] = self.configSections[sectionName].getAllSectionSettings()

    def readConfigFile(self):
        """"""
        with open(self.__configFileName__, "r", encoding="utf-8") as f:
            self.config.read_file(f)
        self.updateAllSectionsFromConfig()
    
    def updateAllSectionsFromConfig(self):
        """"""
        for sectionName in self.config.sections():
            if sectionName in self.configSections:
                self.configSections[sectionName].updateAllSectionSettings(dict(self.config.items(sectionName)))
            else:
                raise KeyError(f"ERROR: ConfigFile '{self.__configFileName__}' section name '{sectionName}' is not " + 
                               "a know section name. Is the section name spelled correctly?")
    
    def writeConfigFile(self):
        """"""
        with open(self.__configFileName__, "w", encoding="utf-8") as f:
            self.config.write(f)

    def printConfig(self):
        """"""
        print("Current configuration tree:")
        for sName in self.config.sections():
            for oName in self.config.options(sName):
                print(f"[{sName}][{oName}]'{self.config.get(sName, oName)}'")


# End of class className

# -----------------------------------------------------------------------------

# Define the "Main" Function. If this is not the program module this function can be used for isolated debug testing by executing this file.
def main() -> int:
    """This is the "Main" function which is called automatically by the last two lines if this is the top level Module. 'Import this_file' will not call main().
    """
    import argparse
    pCmdLine = argparse.ArgumentParser()
    pCmdLine.add_argument("-f", "--FileName", type=str, help="Use this Configuration File inplace default file.")
    pCmdLine.add_argument("-w", "--writeConfig", action="store_true", help="Write to file is true.")
    pCmdLine.add_argument("-n", "--noReadConfig", action="store_false", help="Write to file is true.")
    args = pCmdLine.parse_args()

    # Import Local modules here.
    from sbSounds import SoundSettingsConfig
    print("Import done for local modules.")
    # Setup Done now run tests
    
    if args.FileName is None:
        fName = "sbSoundsConfig"
    else:
        fName = args.FileName
    conf = configFileParser(fName)
    print("Assign configFileParser object.")

    soundSettings = SoundSettingsConfig()
    print("Assign config sections.")

    conf.registerSettingsSection(soundSettings)
    print("Done Registering config sections")

    soundSettings.printAllSettings()
    conf.printConfig()

    if not args.noReadConfig:
        conf.readConfigFile()

    if args.writeConfig:
        conf.writeConfigFile()

    # Return 0 is considered a “successful termination”; anyother value is seen as an error by the OS.)
    return 0 
# End of main() Function  

# Call main function if this is the top level Module 
if __name__ == '__main__':
    sys.exit(main()) 