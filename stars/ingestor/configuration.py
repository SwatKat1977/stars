'''
Copyright 2019-2021 Image Gopher

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
from config_base import ConfigBase

class Configuration(ConfigBase):
    """ Class defining ingestor service configuration options """

    required_items = {
        'logging':
        {
            'log_level': ('DEBUG', 'INFO')
        },
        'general':
        {
            'import_directory': None
        }
    }

    @property
    def logging_log_level(self) -> str:
        """ Return config item logging | log level """
        return self._logging_log_level

    @property
    def general_import_dir(self) -> str:
        """ Return config item general | import directory root """
        return self._general_import_dir

    def __init__(self, config_file, file_required : bool) -> None:
        super().__init__(config_file, file_required, self.required_items)

        self._logging_log_level = self.read_str('logging', 'log_level', 'INFO')
        self._general_import_dir = self.read_str('general', 'import_directory',
                                                 is_required=True)
