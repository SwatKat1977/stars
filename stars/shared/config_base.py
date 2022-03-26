'''
Copyright 2022 Staff Recruitment System (STARS)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
import configparser
import os
import typing

class ConfigBase(configparser.ConfigParser):
    """
    Base class that handling configuration items from environment variables.
    """

    def __init__(self, config_file : str = None, file_required : bool = False,
                 required_values = None):
        """
        Constructor for the configuration base class, it can take in a config
        file and a dictionary to validate the file.

        Example of required_fields:
        required_config_values = {
            'general':
            {
                'log_level': ('DEBUG', 'INFO')
            },
            'client':
            {
                'import_directory': None
            }
        }

        parameters:
            config_file : Config file to read (optional, default = None)
            file_required : Is the file required (optional, default = False)
            required_files : Dict of required item (optional, default = None)
        """
        super().__init__()

        files_read = []

        self._config_file : str = config_file
        self._has_config_file = False

        if config_file:
            try:
                files_read = self.read(config_file)

            except configparser.ParsingError as ex:
                raise ValueError(
                    f"Failed to read required config file, reason: {ex}") from ex

            if not files_read and file_required:
                raise ValueError(
                    f"Failed to open required config file '{config_file}'")
            if required_values:
                self._validate_config(required_values)

            self._has_config_file = True

    def read_str(self, section : str, option : str, default : str = None,
                 is_required : bool = False) -> str:
        """
        Read a configuration option of type string, firstly it will check for
        an enviroment variable, otherise try the configuration file (if it
        exists). An ValueError exception is thrown it's missing and marked as
        is_required.

        parameters:
            section : Configuration section
            option : Configuration option to read
            default : Default value (if not a required variable)
            is_required : Is a required env variable flag (default is False)

        returns:
            A str or None if it's not a required field.
        """

        value = self._read_from_env_variable(option, default, is_required)

        # If no environment variable is found, check config file (if exits)
        if not value and self._has_config_file:
            try:
                value = self.get(section, option)

            except configparser.NoOptionError:
                value = None

        if not value and is_required:
            raise ValueError(f"Missing required config option '{option}'")

        return value

    def read_int(self, section : str, option : str, default : int = -1,
                 is_required : bool = False) -> int:
        """
        Read a configuration option of type int, firstly it will check for
        an enviroment variable, otherise try the configuration file (if it
        exists). An ValueError exception is thrown it's missing and marked as
        is_required or is not an int.

        parameters:
            section : Configuration section
            option : Configuration option to read
            default : Default value (if not a required variable)
            is_required : Is a required env variable flag (default is False)

        returns:
            An int or None if it's not a required field.
        """

        value = self._read_from_env_variable(option, default, is_required)

        # If no environment variable is found, check config file (if exits)
        if not value and self._has_config_file:
            try:
                self.getint(section, option)

            except configparser.NoOptionError:
                value = None

            except ValueError as ex:
                raise ValueError((f"Configuration option '{option}' is not a "
                                   "valid int.")) from ex

        if not value and is_required:
            raise ValueError(f"Missing required config option '{option}'")

        try:
            value = int(option)

        except ValueError as ex:
            raise ValueError((f"Configuration option '{option}' with a value "
                             f" of '{value}' is not an int.")) from ex

        return value

    def _read_from_env_variable(self, key : str, default_value : typing.Any,
                                is_required : bool) -> str:
        # pylint: disable=no-self-use
        """
        Read a value from enviroment variable.

        parameters:
            key : Environment variable key name
            default_value : Default value (if not a required variable)
            is_required : Is a required env variable flag

        returns:
            A str or None if it's not a required field.
        """

        env_variable_default = None if is_required else default_value
        key_value = os.getenv(key, env_variable_default)

        return key_value

    def _validate_config(self, required_values : dict):

        for section, keys in required_values.items():
            if section not in self:
                raise ValueError(
                    f"Missing config file section '{section}'")

            for key, values in keys.items():
                self._validate_section_key(section, key, values)

    def _validate_section_key(self, section : str, key : str, values :str):

        if key not in self[section] or self[section][key] == '':
            raise ValueError((
                'Missing value for %s under section %s in ' +
                'the config file') % (key, section))

        if values and self[section][key] not in values:
            raise ValueError((
                'Invalid value for %s under section %s in ' +
                'the config file') % (key, section))

required_config_values = {
    'general':
    {
        'log_level': ('DEBUG', 'INFO'),
        'mode': ('master')
    },
    'client':
    {
        'import_directory': None
    }
}

try:
    d = ConfigBase('None', True, required_config_values)
    #d.read_int('client', 'import_directory', None)
    client_dir = d.read_str('client', 'import_directory', None)
    print('client dir', client_dir)
    print('--------------------------------')
    d.read_int('client', 'import_directory', is_required=True)

except ValueError as test_except:
    print(test_except)
