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
import logging
import time
import configuration
import version

class MainProcess:
    """ Worker processor base class """
    __slots__ = ["_config", "_logger", "_shutdown_completed",
                 "_shutdown_requested"]

    def __init__(self, logger : logging.Logger, 
                 config : configuration.Configuration):
        self._config = config
        self._logger = logger.getChild(__name__)
        self._shutdown_completed : bool = False
        self._shutdown_requested : bool = False

    def initialise(self) -> bool:

        opt_tag = f"-{version.VERSION_OPT_TAG}" \
            if version.VERSION_OPT_TAG != "" else ""
        version_str = (f"V{version.VERSION_MAJOR}."
                       f"{version.VERSION_MINOR}."
                       f"{version.VERSION_PATCH}{opt_tag}")
        self._logger.info("Staff Recruitment System Ingestor Service %s",
                          version_str)
        self._logger.info("Licensed under the Apache License, Version 2.0")
        self._logger.info("-------------------------------------")
        self._logger.info("Configuration items")
        self._logger.info("= Logger items =")
        self._logger.info("|=> Log level: %s", self._config.logging_log_level)
        self._logger.info("= General items =")
        self._logger.info("|=> Import directory root : %s",
                          self._config.general_import_dir)
        self._logger.info("-------------------------------------")

        return True

    def run(self) -> None:

        while not self._shutdown_requested:
            try:
                self._main_loop()
                time.sleep(0.1)

            except KeyboardInterrupt:
                break

        self._logger.info("Exiting Application process...")

        self._shutdown_completed = True

    def stop(self) -> None:
        self._logger.info("Stopping Application process...")

        self._shutdown_requested = True

        while not self._shutdown_completed:
            ''' '''
            time.sleep(0.1)

        self._logger.info("Application process shutdown has completed")

        self._shutdown()

    def _main_loop(self) -> None:
        ## The main loop code goes here...
        ...

    def _shutdown(self) -> None:
        ...
