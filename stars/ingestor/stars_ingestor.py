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
import logging
import os
import configuration

def main():
    config_file = os.getenv("INGESTOR_CONFIG_FILE", None)
    config_file_required = os.getenv("INGESTOR_CONFIG_FILE_REQUIRED", True)

    if not config_file and config_file_required == 1:
        print("[FATAL ERROR] Configuration file missing!")
        return

    try:
        config = configuration.Configuration(config_file, config_file_required)

    except ValueError as ex:
        print(f"[FATAL ERROR] Configuration error : {ex}")
        return

    # Configure logging.
    logger = logging.getLogger(__name__)
    log_format= logging.Formatter("%(asctime)s [%(levelname)s] %(message)s",
                                  "%Y-%m-%d %H:%M:%S")
    console_stream = logging.StreamHandler()
    console_stream.setFormatter(log_format)
    logger.addHandler(console_stream)
    logger.setLevel(config.logging_log_level)
    logger.info("Logging level: %s", config.logging_log_level)

if __name__ == "__main__":
    main()
