# filename.py
# sbSounds.py
# 
# Description: 
# 
#

#import sys   # System-specific parameters and functions
#import os    # Miscellaneous operating system interfaces  

from numbers import Number
import numbers
from re import S

ENABLE_thisIsExecuting_TO_PRINT = False
if ENABLE_thisIsExecuting_TO_PRINT: 
    #from functools import partial
    from inspect import stack
    def thisIsExecuting() -> None:
        """"""
        s = [""]
        for fr in stack():
            s.append(f"{fr.function}")
        print(f"Traceback: {"->".join(s)}")
        #print(f"Traceback: {classInstance.__qualname__}.{callerName}: {txt}")
else:
    def thisIsExecuting() -> None:
        """Set 'ENABLE_methodIsExecuting_TO_PRINT = True' to enable this function before this function is imported."""
        pass


class ConfigSetting:
    """"""

    def __set_name__(self, owner, name: str) -> None:
        """"""
        if isinstance(name, str):
            if len(name) > 0:
                # The Stores the name of the Section in the config file.  
                self.__name__ = name
            else:
                raise ValueError("Argument 'name' is to Short: 'name' needs to be a string of length greather than 0.")
        elif name == None:
            raise ValueError("Argument 'name' equals None: 'name' needs to be a string of length greather than 0.")
        else:
            raise TypeError(f"Argument type(name) = {type(name)}: 'name' needs to be a string of length greather than 0.")
        o: ConfigSettingsBase = owner
        try:
            if len(o.__configSection_Name__) > 0:
                self.__sectionName__: str = o.__configSection_Name__
            else:
                self.__sectionName__: str = o._configDefaultSection_Name
            #print(f"Registering Setting: '{o.__qualname__}.{name}' in section '{self.__sectionName__}'")
            if self.__sectionName__ not in o._allConfigSettings:
                o._allConfigSettings[self.__sectionName__] = {}
            o._allConfigSettings[self.__sectionName__][name] = self
        except AttributeError as err:
            raise TypeError("\n".join(["This class expects to be assigned as an attribute inside the class ConfigSettingsBase or its subclasses.", 
                                      f"This instance was assigned in class, {type(o)}, to attribute: '{name}'"])) from err

    def __init__(self, defaultValue) -> None:
        """"""
        thisIsExecuting()
        #print(f"Initialising a configuration setting to '{defaultValue}'")
        if isinstance(defaultValue, bool):
            raise TypeError("Use ConfigSettingBool for a boolean type")
        self.__value__ = defaultValue
        self.valType = type(defaultValue)

    def __get__(self, instance, owningClass=None):
        """"""
        return self.__value__
    
    def __set__(self, instance, value):
        """"""
        raise AttributeError(f"{self.__name__} is a READ ONLY attribute. Use class (or a subclass of) ConfigSettingsBase's update* Methods.")

    def __str__(self) -> str:
        """
        __str__ is called by str(object), the default __format__() implementation, and the built-in function 
            print(), to compute the “informal” or nicely printable string representation of an object. 
            The return value must be a str object. The default implementation defined by the built-in type object 
            calls object.__repr__().

        :return: A string representation of the value. 
        :rtype: str
        """
        return str(self.__value__)
    
    def updateFromSettingsDict(self, settings: dict[str, str]):
        """"""
        valueString = settings[self.__name__]
        try:
            if len(valueString) < 1:
                raise ValueError("Config Error: '{0:s}:{1:s}' has no value in the config file."
                        .format(self.__sectionName__,self.__name__))
            self.__value__ = self.convertStr2ValueType(valueString)
        except ValueError as valErr:
            msg = f"Config Error: while updating config setting '{self.__name__}' to '{valueString}'.\n" + \
                    f"The conversion from 'str' to '{self.valType}' failed."
            if self.__value__ is None:
                valErr.add_note(msg + "Default value not present therefore cannot procede.")
                raise 
            else:
                print(msg + "Therefore the default value will be used.")

    def convertStr2ValueType(self, valueString: str):
        """"""
        return self.valType(valueString)
# End of class ConfigSetting

class ConfigSettingBool(ConfigSetting):
    """"""
    def __init__(self, defaultValue) -> None:
        """"""
        #print(f"Initialising a Boolean configuration setting to '{defaultValue}'")
        self.valType = bool
        if isinstance(defaultValue, bool):
            self.__value__ = defaultValue
        elif isinstance(defaultValue, numbers.Number):
            if defaultValue == 0:
                self.__value__ = False
            else:
                self.__value__ = True
        elif isinstance(defaultValue, str):
            self.__value__ = self.convertStr2ValueType(defaultValue)
        else:
            self.__value__ = self.convertStr2ValueType(str(defaultValue))

    def __bool__(self) -> bool:
        return self.__value__

    def convertStr2ValueType(self, valueString: str) -> bool:
        """
        convertStr2ValueType does a match reguarless of case to return True or False. If a match is not 
        found a ValueError is raized.
        Returns True if valueString matches a trueString: "true", "1", "on", "yes"
        Returns False if valueString matches a falseString: ["true", "1", "on", "yes"]

        :param valueString: Description
        :type valueString: str
        :return: True if trueString is matched. False of a falseString is matched.
        :rtype: bool
        """
        boolText = {"true": True, "1": True, "on": True, "yes": True, 
                    "false": False, "0": False, "off": False, "no": False}
        s = valueString.lower().strip()
        if s in boolText:
            return boolText[s]
        else:
            raise ValueError(f"ERROR: Unable to Convert '{valueString}' to a bool. This method's Docstring:\n" + 
                                    "")
# End of class ConfigSettingBool

# Instantiation Syntax: ConfigSettingsBase()
class ConfigSettingsBase:
    """
    ConfigSettingsBase is the basic settings configuration class.  This class should be used 
    as the base class for application specific classes to inherit the common functionality 
    functions.
    If subclasses override __init__() running 'super().__init__()' to execute this class's __init__().

    To make a configuration section subclassing this class and override '__configSection_Name__'
    by setting it equal to the desired section name.
    """
    _configDefaultSection_Name = "Common Settings"
    __configSection_Name__ = ""
    __configSettings__: dict[str, ConfigSetting] = {}   # TODO Deleat this attribute. It is deprecated.
    _allConfigSettings: dict[str, dict[str, ConfigSetting]] = {}

    Debuging = ConfigSettingBool("Yes") # declarese if debuging is happening.
    Verbosity_Level = ConfigSetting(2)

    # Customize the current instance to a specific initial state.
    def __init__(self, updateFromConfigFile: bool = True) -> None:
        """
        __init__ initializes the current instance of ConfigSettingsBase. 
        
        :param configFileSectionName: Must be a string of length > 0
        :type configFileSectionName: str
        :param updateFromConfigFile: Optional, defaults to False, When True this class expects settings to be 
                updated from the config file as read by the configparser.ConfigParser
        :type updateFromConfigFile: bool
        """
        #print(f"In ConfigSettingsBase's __init__(); updateFromConfigFile = {updateFromConfigFile}")
        if isinstance(updateFromConfigFile, bool) and not updateFromConfigFile:
            self.__allSectionSsettingsUpdated__ = True 
        else:
            self.__allSectionSsettingsUpdated__ = False
    # End of __init__() Method

    def getSectionName(self) -> str: 
        """Returns the name of the section where these seetings are stored. {self:'instanceName'}.sectionName will invoke this getter."""
        return self.__configSection_Name__
    def getDefaultSectionName(self) -> str: 
        """Returns the name of the default section where common settings are stored. {self:'instanceName'}.sectionName will invoke this getter."""
        return self._configDefaultSection_Name

    def getAllSettings(self) -> dict[str, dict[str, str]]:
        """Returns the ALL the configuration settings as a dictionary of strings. {self:'instanceName'}.sectionAllSettings will invoke this getter."""
        settings: dict[str, dict[str, str]] = {}
        for sectName in self._allConfigSettings:
            if sectName not in settings:
                settings[sectName] = {}
            for name, cSetting in self._allConfigSettings[sectName].items():
                settings[sectName][name] = str(cSetting)
        return settings

    def updateSectionSettings(self, settings: dict[str, str]):
        """Sets Config Settings from a ConfigParser instance. {self:'instanceName'}.sectionAllSettings(settings) will invoke this getter."""
        for name, cSetting in self.__configSettings__.items():
            if name in settings:
                cSetting.updateFromSettingsDict(settings)
            else:
                print("Config Warning: '{0:s};{1:s}' is NOT Found in config file./n/t Using default value."
                      .format(self.getSectionName(), name))
        for name in settings.keys():
            if name not in self.__configSettings__:
                print("Config Warning: '{0:s}; {1:s}' is not used./n/t Is it spelled correctly or deprecated?"
                      .format(self.getSectionName(),name))
        self.__allSectionSsettingsUpdated__ = True

    def getSectionSettings(self) -> dict[str, str]:
        """Returns the configuration settings as dictionary of strings. {self:'instanceName'}.sectionAllSettings will invoke this getter."""
        settings = {}
        for name, cSetting in self.__configSettings__.items():
            settings[name] = str(cSetting)
        return settings

    def areSectionSsettingsUpdated(self) -> bool:
        #return self.__settingsLoadedFromConfigFile__
        return self.__allSectionSsettingsUpdated__

    def printSectionSettings(self):
        """"""
        print(f"All settings for section: '{self.getSectionName()}'")
        for name, cSetting in self.__configSettings__.items():
            print(f"   Name: '{name}' Type: {cSetting.valType} Value: '{cSetting}'")

    def printAllSettings(self, stringOnly: bool = False) -> str:
        """"""
        s = [f"All settings for all sections:"]
        for sectName in self._allConfigSettings:
            s.append(f"Section: '{sectName}'")
            for name, cSetting in self._allConfigSettings[sectName].items():
                s.append(f"  Name: '{name}' Type: {cSetting.valType} Value: '{cSetting}'")
        if not stringOnly:
            print("\n".join(s))
        return "\n".join(s)
# End of class ConfigSettingsBase

# -----------------------------------------------------------------------------
# No main function because this Module is designed to only be a base class that 
# is inherited into subclasses.
