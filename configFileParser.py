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
    from sbSounds import SoundSettingsConfig
    soundSettings = SoundSettingsConfig()

    conf = configFileParser("sbSoundsConfig")
    conf.registerSettingsSection(soundSettings)

    conf.printConfig()
    # Return 0 is considered a “successful termination”; anyother value is seen as an error by the OS.)
    return 0 
# End of main() Function  

# Call main function if this is the top level Module 
if __name__ == '__main__':
    sys.exit(main()) 