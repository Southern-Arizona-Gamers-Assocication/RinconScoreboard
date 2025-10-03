# filename.py
# sbSounds.py
# 
# Description: 
# 
# 

#import sys   # System-specific parameters and functions
#import os    # Miscellaneous operating system interfaces  
from typing import Final, final, cast

import numbers

# Define Constents Here
DEFAULT_CONFIG_SECTION_NAME = "Common Settings"
DO_NOT_READ_CONFIG_FILE = True

# Define Functions and Classes Here
class ConfigSetting:
    """"""
    def __set_name__(self, owner, name) -> None:
        """"""
        if isinstance(name, str):
            if len(name) > 0:
                # The Stores the name of the Section in the config file.  
                self.__nameMe__ = name
            else:
                raise ValueError("Argument 'name' is to Short: 'name' needs to be a string of length greather than 0.")
        elif name == None:
            raise ValueError("Argument 'name' equals None: 'name' needs to be a string of length greather than 0.")
        else:
            raise TypeError(f"Argument type(name) = {type(name)}: 'name' needs to be a string of length greather than 0.")
        o: ConfigSettingsBase = owner
        self.owningClass = o
        errorTextStart = "A config setting name must be unique accross all sections."
        try:
            if len(o._configSection_Name) > 0:
                self.__sectionName__: str = o._configSection_Name
            else:
                self.__sectionName__: str = o._configDefaultSection_Name
            # if hasattr(o, name):
            #     print(f"'{self.__sectionName__}'.{name} already exists and has id:{id(getattr(o,name)):#x} {'==' if id(getattr(o,name)) == id(self) else '!='} Current id:{id(self):#x}.")
            # print(f"<{self.__sectionName__}.{name} at {id(self):#x}> Setting Name. Owning Class: <{o} at {id(o):#x}>")
            # if name in o._configSettingsByName:
            #     print(f"<{o._configSettingsByName[name].__sectionName__}.{o._configSettingsByName[name].__nameMe__} at {id(o._configSettingsByName[name]):#x}> Duplicates Current Setting.")
            #     #raise AttributeError(f"{errorTextStart}\nThis setting, '{self.__sectionName__}'.{name}, is also in '{o._configSettingsByName[name].__sectionName__}'.", name=name, obj=o)
            o._configSettingsByName[name] = self
            if self.__sectionName__ not in o._configSettingsBySection:
                o._configSettingsBySection[self.__sectionName__] = {}
            o._configSettingsBySection[self.__sectionName__][name] = self
        except AttributeError as err:
            if any([(errorTextStart in s) for s in err.args]):
                raise
            else:
                raise TypeError("\n".join(["This class expects to be assigned as an attribute inside the class ConfigSettingsBase or its subclasses.", 
                                        f"This instance was assigned in class, {type(o)}, to attribute: '{name}'"])) from err
    def __init__(self, defaultValue) -> None:
        """"""
        #thisIsExecuting()
        #print(f"<{type(self).__qualname__} at {id(self):#x}> Initialising to '{defaultValue}'")
        if isinstance(defaultValue, bool):
            raise TypeError("Use ConfigSettingBool for a boolean types")
        self.__value__ = defaultValue
        self.valType = type(defaultValue)

    def get_name(self) -> str:
        """"""
        return self.__nameMe__

    def __get__(self, instance, owningClass=None):
        """"""
        return self.__value__
    
    def __set__(self, instance, value):
        """"""
        raise AttributeError(f"{self.__nameMe__} is a READ ONLY attribute. Use class (or a subclass of) ConfigSettingsBase's update* Methods.")

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
        valueString = settings[self.__nameMe__]
        try:
            if len(valueString) < 1:
                raise ValueError(f"Config Error: '{self.__sectionName__}:{self.__nameMe__}' has no value in the config file.")
            self.__value__ = self.convertStr2ValueType(valueString)
        except ValueError as valErr:
            msg = f"Config Error: while updating config setting '{self.__nameMe__}' to '{valueString}'.\n" + \
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
        #print(f"<{type(self).__qualname__} at {id(self):#x}> Initialising to '{defaultValue}'")
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

class ConfigSettingsBase:
    """
    ConfigSettingsBase is the basic settings configuration class.  This class should be used 
    as the base class for application specific classes to inherit the common functionality 
    functions.
    If subclasses override __init__() running 'super().__init__()' to execute this class's __init__().

    To make a configuration section subclassing this class and override '__configSection_Name__'
    by setting it equal to the desired section name.
    """
    _configDefaultSection_Name: Final[str] = DEFAULT_CONFIG_SECTION_NAME
    _configSection_Name = ""
    _configSettingsByName: Final[dict[str, ConfigSetting]] = {} 
    _configSettingsBySection: Final[dict[str, dict[str, ConfigSetting]]] = {}

    Config_Settings_Base = ConfigSetting("Config_Settings_Base")
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
        if not isinstance(self._configSection_Name, str) or len(self._configSection_Name) < 1:
            raise ValueError(f"{ConfigSettingsBase.__name__} is expected to be a base class with the Subclasses " +
                              "overriding _configSection_Name to the unique name of the corrisponding section in " +
                              "the configuration file.")
        print(f"In ConfigSettingsBase's __init__(); for {type(self)}")
        if isinstance(updateFromConfigFile, bool) and not updateFromConfigFile:
            self.__allSectionSsettingsUpdated = True 
        else:
            self.__allSectionSsettingsUpdated = False
    # End of __init__() Method

    def getSectionName(self) -> str: 
        """Returns the name of the section where these seetings are stored. {self:'instanceName'}.sectionName will invoke this getter."""
        return self._configSection_Name
    def getDefaultSectionName(self) -> str: 
        """Returns the name of the default section where common settings are stored. {self:'instanceName'}.sectionName will invoke this getter."""
        return self._configDefaultSection_Name

    def getAllSettings(self) -> dict[str, dict[str, str]]:
        """Returns the ALL the configuration settings as a dictionary of strings. {self:'instanceName'}.sectionAllSettings will invoke this getter."""
        settings: dict[str, dict[str, str]] = {}
        for sectName in self._configSettingsBySection:
            if sectName not in settings:
                settings[sectName] = {}
            for name, cSetting in self._configSettingsBySection[sectName].items():
                settings[sectName][name] = str(cSetting)
        return settings

    def areSettingsUpdatedFromConfigFile(self) -> bool:
        #return self.__settingsLoadedFromConfigFile__
        return self.__allSectionSsettingsUpdated

    # def updateSectionSettings(self, settings: dict[str, str]):
    #     """Sets Config Settings from a ConfigParser instance. {self:'instanceName'}.sectionAllSettings(settings) will invoke this getter."""
    #     for name, cSetting in self.__configSettings__.items():
    #         if name in settings:
    #             cSetting.updateFromSettingsDict(settings)
    #         else:
    #             print("Config Warning: '{0:s};{1:s}' is NOT Found in config file./n/t Using default value."
    #                   .format(self.getSectionName(), name))
    #     for name in settings.keys():
    #         if name not in self.__configSettings__:
    #             print("Config Warning: '{0:s}; {1:s}' is not used./n/t Is it spelled correctly or deprecated?"
    #                   .format(self.getSectionName(),name))
    #     self.__allSectionSsettingsUpdated = True

    # def getSectionSettings(self) -> dict[str, str]:
    #     """Returns the configuration settings as dictionary of strings. {self:'instanceName'}.sectionAllSettings will invoke this getter."""
    #     settings = {}
    #     for name, cSetting in self.__configSettings__.items():
    #         settings[name] = str(cSetting)
    #     return settings

    # def printSectionSettings(self):
    #     """"""
    #     print(f"All settings for section: '{self.getSectionName()}'")
    #     for name, cSetting in self.__configSettings__.items():
    #         print(f"   Name: '{name}' Type: {cSetting.valType} Value: '{cSetting}'")

    def printAllSettings(self, stringOnly: bool = False) -> str:
        """"""
        s = [f"All settings for all sections:"]
        for sectName in self._configSettingsBySection:
            s.append(f"Section: '{sectName}'")
            for name, cSetting in self._configSettingsBySection[sectName].items():
                s.append(f"  Name: '{name}' Type: {cSetting.valType} Value: '{cSetting}'")
        if not stringOnly:
            print("\n".join(s))
        return "\n".join(s)
# End of class ConfigSettingsBase

class _dummyConfigSettingsBaseClass:
    """This is a Dummy Class and a placeholder ConfigSettingsBase to be assigned to settings in SubSystemConfigBase. 
        SubSystemConfigBase.settings should be overridden by a proper subclass of ConfigSettingsBase."""
    def areSettingsUpdatedFromConfigFile(self) -> bool:
        """his is a Dummy Function that returns True and does no checking."""
        return True
    
class SubSystemConfigBase:
    """"""
    # Override this in the subclass by the customized settings
    #settings = ConfigSettingsBase()
    
    def __init__(self) -> None:
        """Init Sound subsystem"""
        self.__preSetupGetExternalData: bool = False

    settings = _dummyConfigSettingsBaseClass()

    def preSetupPostSettingsUpdateGetExternalData(self):
        """"""
        if DO_NOT_READ_CONFIG_FILE or self.settings.areSettingsUpdatedFromConfigFile() or (__name__ != 'scoreboard.py'):
            self.__preSetupGetExternalData = True
        else:
            raise RuntimeError("Configuration file has not been read to update settings.")

    def isReadyToSetup(self) -> bool:
        """IF Overriding this Method, THis one NEEDS to be called. Ex 'super().isReadyToSetup()'.
            isReadyToSetup() returns True of the subsystem is ready to start, False otherwise."""
        if not self.__preSetupGetExternalData:
            return False
        return True

    def setupSubSys(self) -> None:
        """IF Overriding this Method, THis one NEEDS to be called on the first line. Ex 'super().setupSubSys()'.
            If not ready to set up this will Raise a RuntimeError."""
        if not self.isReadyToSetup():
            raise RuntimeError(f"{self.__class__.__name__}.isReadyToSetup() returned False. Check setup chain.")

    def shutdownSubSys(self) -> None:
        """"""
        pass
# End of class ConfigSettingsBase

# -----------------------------------------------------------------------------
# No main function because this Module is designed to only be a base class that 
# is inherited into subclasses.
