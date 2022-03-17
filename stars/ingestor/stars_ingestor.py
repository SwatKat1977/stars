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

def main():

    # Configure logging.
    logger = logging.getLogger(__name__)
    log_format= logging.Formatter("%(asctime)s [%(levelname)s] %(message)s",
                                  "%Y-%m-%d %H:%M:%S")
    console_stream = logging.StreamHandler()
    console_stream.setFormatter(log_format)
    logger.addHandler(console_stream)
    logger.setLevel(logging.DEBUG)
    logger.info("Logging level: DEBUG")

if __name__ == "__main__":
    main()
