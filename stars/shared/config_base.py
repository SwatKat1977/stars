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
from os import getenv
from typing import Any

class ConfigBase:
    """
    Base class that handling configuration items from environment variables.
    """
    # pylint: disable=no-self-use

    def read_str_from_env_variable(self, key : str, default_value : str,
                                   is_required : bool = False) -> str:
        """
        Read a value from enviroment variable. a ValueError exception is thrown
        it's missing and marked as is_required.

        parameters:
            key : Environment variable key name
            default_value : Default value (if not a required variable)
            is_required : Is a required env variable flag (default is False)

        returns:
            A str or None if it's not a required field.
        """
        return self._read_from_env_variable(key, default_value, is_required)

    def read_int_from_env_variable(self, key : str, default_value : int,
                                   is_required : bool = False) -> int:
        """
        Read a value from enviroment variable and attempt to convert it into an
        int. A ValueError exception is thrown if this fails or it's missing and
        marked as is_required.

        parameters:
            key : Environment variable key name
            default_value : Default value (if not a required variable)
            is_required : Is a required env variable flag (default is False)

        returns:
            An int or None if it's not a required field.
        """
        key_value = self._read_from_env_variable(key, default_value,
                                                 is_required)

        try:
            return int(key_value)

        except ValueError as ex:
            exception_msg = (
                f"The setting environebt variable '{key}' with a value "
                f" of '{key_value}' is not an int.")

            raise ValueError(exception_msg) from ex

    def _read_from_env_variable(self, key : str, default_value : Any,
                                is_required : bool) -> str:
        """
        Read a value from enviroment variable. A ValueError exception is thrown
        if it's missing and marked as is_required.

        parameters:
            key : Environment variable key name
            default_value : Default value (if not a required variable)
            is_required : Is a required env variable flag

        returns:
            A str or None if it's not a required field.
        """

        env_variable_default = None if is_required else default_value
        key_value = getenv(key, env_variable_default)

        if key_value is None and is_required:
            raise ValueError(f"Missing required environment variable '{key}'")

        return key_value
