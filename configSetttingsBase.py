# filename.py
# sbSounds.py
# 
# Description: 
# 
#

#import sys   # System-specific parameters and functions
#import os    # Miscellaneous operating system interfaces  
#from configparser import ConfigParser

# Instantiation Syntax: ConfigSettingsBase()
class ConfigSettingsBase:
    """
    ConfigSettingsBase is the basic settings configuration class.  This class should be used 
    as the base class for application specific classes to inherit the common functionality 
    functions.
    """
    # Customize the current instance to a specific initial state.
    def __init__(self, configFileSectionName: str = "") -> None:
        """
        __init__ initializes the current instance of ConfigSettingsBase. 
        
        :param configFileSectionName: Description
        :type configFileSectionName: str
        """
        # Execute the a base classes __init__() 
        #super().__init__(configFileSectionName)
        print(f"Initializing ConfigSettingsBase with a Section Name = '{configFileSectionName}'")
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
        #self.__configSettings__ = {}
        self.__allSectionSsettingsUpdated__ = False 

    class ConfigSetting:
        """"""
        def __set_name__(self, owner, name) -> None:
            print(f"Name is set for '{owner}.{name}'")
            if hasattr(owner, name):
                raise AttributeError(f"Name '{name}' is already used in the {owner.__class__.__name__} class.")
            self.__name__ = name
            self.__owner__ = owner
            owner.__configSettings__[name] = self
        
        def __init__(self, defaultValue) -> None:
            print(f"Setting default value: '{defaultValue}'")
            self.__value__ = defaultValue
            self.valType = type(defaultValue)

        def __get__(self, instance, owningClass=None):
            """"""
            return self.__value__
        
        def __set__(self, instance, value):
            """"""
            raise AttributeError(f"{self.__name__} is a READ ONLY configuration setting. Use .setAllSectionSettings() to configure from config file.")

        def __str__(self) -> str:
            """
            __str__ is called by str(object), the default __format__() implementation, and the built-in function 
                print(), to compute the “informal” or nicely printable string representation of an object. 
                The return value must be a str object. The default implementation defined by the built-in type object 
                calls object.__repr__().

            :return: A string representation of the value. 
            :rtype: str
            """
            print(f"Outputing {self.__name__} as a String Value")
            return self.__value__.__repr__()
        
        def updateFromSettingsDict(self, settings: dict[str, str]):
            """"""
            valueString = settings[self.__name__]
            try:
                if len(valueString) < 1:
                    raise ValueError("Config Error: '{0:s}:{1:s}' has no value in the config file."
                          .format(self.__owner__.sectionName(),self.__name__))
                self.__value__ = self.convertStr2ValueType(valueString)
            except ValueError as valErr:
                msg = f"Config Error: while updating config setting '{self.__name__}' to '{valueString}'.\n" + \
                      f"The conversion from 'str' to '{self.valType}' failed."
                if self.__value__ is None:
                    valErr.add_note(msg + "Default value not present therefore cannot procede.")
                    raise 
                else:
                    print(msg + "Therefore the defalt value will be used.")

        def convertStr2ValueType(self, valueString: str):
            """"""
            return self.valType(valueString)
    # End of class ConfigSetting

    class ConfigSettingBool(ConfigSetting):
        """"""
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
            match valueString.lower():
                case ["true", "1", "on", "yes"]:
                    return True
                case ["false", "0", "off", "no"]:
                    return False
                case _:
                    raise ValueError("")
    # End of class ConfigSettingBool

    __configSettings__: dict[str, ConfigSetting] = {}

    def sectionName(self) -> str: 
        """Returns the name of the section where these seetings are stored. {self:'instanceName'}.sectionName will invoke this getter."""
        return self.__configSection_Name__

    def getAllSectionSettings(self) -> dict[str, str]:
        """Returns the configuration settings as dictionary of strings. {self:'instanceName'}.sectionAllSettings will invoke this getter."""
        settings = {}
        for name, value in self.__configSettings__.items():
            settings[name] = str(value)
        return settings

    def setAllSectionSettings(self, settings: dict[str, str]):
    #def sectionSettings(self, config: configparser.ConfigParser):
        """Sets Config Settings from a ConfigParser instance. {self:'instanceName'}.sectionAllSettings(settings) will invoke this getter."""
        #settings_test = config[self.sectionName]
        print("'Debug --> type(settings) {0:s} ".format(type(settings)))
        for name, cSetting in self.__configSettings__.items():
            print("Settings value '{0:s};{1:s}' = '{2:s}' is a {3:s}./n * Config File Entry value: '{4:s}'"
                  .format(self.sectionName, name, cSetting, cSetting.valType, settings[name]))
            if name in settings:
                cSetting.updateFromSettingsDict(settings)
            else:
                print("Config Warning: '{0:s}; {1:s}' is NOT Found in config file./n/t Using default value."
                      .format(self.sectionName,name))
        for name in settings.keys():
            if name not in self.__configSettings__:
                print("Config Warning: '{0:s}; {1:s}' is not used./n/t Is it spelled correctly or deprecated?"
                      .format(self.sectionName,name))
        self.__allSectionSsettingsUpdated__ = True

    def allSectionSsettingsAreUpdated(self) -> bool:
        #return self.__settingsLoadedFromConfigFile__
        return self.__allSectionSsettingsUpdated__
# End of class ConfigSettingsBase

# -----------------------------------------------------------------------------
# No main function because this Module is designed to only be a base class that 
# is inherited into subclasses.
