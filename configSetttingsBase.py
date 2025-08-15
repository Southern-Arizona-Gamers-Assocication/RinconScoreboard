# filename.py
# sbSounds.py
# 
# Description: 
# 
#

#import sys   # System-specific parameters and functions
#import os    # Miscellaneous operating system interfaces
import configparser
from functools import partial, partialmethod
from typing import Any

# ConfigSettings description: This is the basic settings configuration class.  This class 
#           should be used as the base class for application specific classes to inherit
#           the common functionality functions.  
# Instantiation Syntax: ConfigSettings()
class ConfigSettingsBase:

    # Customize the current instance to a specific initial state.
    def __init__(self, configFileSectionName: str = ""):
        # Execute the a base classes __init__() 
        #super().__init__(configFileSectionName)
        if type(configFileSectionName) is str:
            if len(configFileSectionName) > 0:
                # The Stores the name of the Section in the config file.  
                self.__configSection_Name__ = configFileSectionName
            else:
                raise ValueError("Argument is to Short: configFileSectionName needs to be a string with a length greather than 0")
        elif configFileSectionName == None:
            raise TypeError("Argument Needed: configFileSectionName needs to be a string with a length greather than 0")
        else:
            raise TypeError("Argument Wrong Type: configFileSectionName needs to be a string with a length greather than 0")
        self.__configSettings__ = {}
        self.__settingsLoadedFromConfigFile__ = False 
    
    def _addConfigSetting(self, configFileSettingName: str, defaultValue, docString: str = ""):
        """This function adds a config setting to the instance of this class and returns a new partialmethod descriptor pointing to its getter."""
        self.__isValidConfigFileSettingName__(configFileSettingName, True)
        x = partialmethod(self.__getConfigSetting__, configFileSettingName)
        self.__configSettings__[configFileSettingName] = defaultValue
        return property(partialmethod(self.__getConfigSetting__, configFileSettingName),None,None, docString)

    def __getConfigSetting__(self, configFileSettingName: str) -> Any:
        """This function is primarily used as a getter for the settings stored in this (or an inherited) class."""
        self.__isValidConfigFileSettingName__(configFileSettingName, False)
        # All checks passed return value
        return self.__configSettings__[configFileSettingName]

    def __isValidConfigFileSettingName__(self, configFileSettingName: str, isNameNew: bool = False) -> bool:
        """This function returns True if the setting name is valid and raises an exception otherwise."""
        if type(configFileSettingName) is str:
            if len(configFileSettingName) > 0:
                if isNameNew:
                    # isNameNew = True
                    if configFileSettingName in self.__configSettings__:
                        raise KeyError("Error Adding Setting: {} is already a setting name and settings names MUST be unique."
                                    .format(configFileSettingName))
                else:
                    # isNameNew = False: tryign to read Setting
                    if configFileSettingName not in self.__configSettings__:
                        raise KeyError("Error Reading Setting: {} is not a current setting."
                                    .format(configFileSettingName))
            else:
                raise ValueError("Argument is to Short: configFileSettingName needs to be a string with a length greather than 0")
        elif configFileSettingName == None:
            raise TypeError("Argument Needed: configFileSettingName needs to be a string with a length greather than 0")
        else:
            raise TypeError("Argument Wrong Type: configFileSettingName needs to be a string with a length greather than 0")
        # All checks passed return True.
        return True

    # Override these two _allLocalSettings{Getter:Setter} in inherited class to use special rules for 
    def _allLocalSettingsGetter(self, name, settings) -> bool:
        ''' Special Rules for local Sectins. Overrite in inherited class. If special setting used Return True, if not Return False.'''
        if name == None:  #Should never be true. Customize in inherited class.
            pass
        else:       # None of the if or elif statements were True so return false.
            return False
        return True # An if or elif statements were True.

    def _allLocalSettingsSetter(self, name, settings) -> bool:
        ''' Special Rules for local Sectins. Overrite in inherited class. If special setting used Return True, if not Return False.'''
        if name == None:  #Should never be true. Customize in inherited class.
            pass
        else:       # None of the if or elif statements were True so return false.
            return False
        return True # An if or elif statements were True.

    # Define Common Getters and Setters for Properties. 
    @property
    def sectionName(self) -> str: 
        """Returns the name of the section where these seetings are stored. {self:'instanceName'}.sectionName will invoke this getter."""
        return self.__configSection_Name__

    @property
    def sectionAllSettings(self) -> dict:
        """Returns the configuration settings as dictionary of strings. {self:'instanceName'}.sectionAllSettings will invoke this getter."""
        settings = {}
        for name, value in self.__configSettings__.items():
            if self._allLocalSettingsGetter(name, settings):
                pass
            elif value.isinstance(str):
                settings[name] = value
            else:
                settings[name] = str(value)
        return settings

    @sectionAllSettings.setter
    def sectionAllSettings(self, settings):
    #def sectionSettings(self, config: configparser.ConfigParser):
        """Sets Config Settings from a ConfigParser instance. {self:'instanceName'}.sectionAllSettings(settings) will invoke this getter."""
        #settings_test = config[self.sectionName]
        print("'Debug --> type(settings) {0:s} ".format(type(settings)))
        for name, value in self.__configSettings__.items():
            print("Settings value '{0:s};{1!s}' = '{2:s}' is a {3:s}./n * Config File Entry value: '{4:s}'"
                  .format(self.sectionName, name, value, type(value), settings[name]))
            if name in settings:
                if self._allLocalSettingsSetter(name, settings):
                    pass
                elif settings[name].len() < 1:
                    print("Config Error: '{0:s}; {1:s}' has no value in the config file."
                          .format(self.sectionName,name))
                elif value.isinstance(str):
                    self.__configSettings__[name] = settings[name]
                elif value.isinstance(int):
                    self.__configSettings__[name] = int(settings[name])
                elif value.isinstance(float):
                    self.__configSettings__[name] = float(settings[name])
                else:
                    print("Config Error: Setting '{0:s};{1!s}' = '{2:s}' is a {3:s}/n  was not processed. Config File value: '{4:s}' will not be used."
                          .format(self.sectionName, name, value, type(value), settings[name]))
            else:
                print("Config Warning: '{0:s}; {1:s}' is NOT Found in config file./n/t Using default value."
                      .format(self.sectionName,name))
        for name in settings.key():
            if name not in self.__configSettings__:
                print("Config Warning: '{0:s}; {1:s}' is not used./n/t Is it spelled correctly or deprecated?"
                      .format(self.sectionName,name))
        self.__settingsLoadedFromConfigFile__ = True

    def haveSettingBeenLoadedFromConfigFile(self) -> bool:
        #return self.__settingsLoadedFromConfigFile__
        return True # Set to false when Config file subsystem has been loaded.

# -----------------------------------------------------------------------------
# No main function because this Module is designed to only be a base class that 
# is inherited into subclasses.
