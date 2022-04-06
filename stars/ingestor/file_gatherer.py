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
import hashlib
import logging
import os
import time
import magic
import file_type

class FileGatherer:
    """ Class that manages gathering a list of fils to import """
    __slots__ = ["_import_directory", "_logger"]

    FILETYPE_PDF = "PDF document"
    FILETYPE_TEXT = "ASCII text"
    FILETYPE_WORD = "Microsoft Word"

    @property
    def import_directory(self) -> str:
        """
        Get the import directory.

        returns:
            Import directory.
        """
        return self._import_directory

    @import_directory.setter
    def import_directory(self, value : str):
        self._import_directory = value

    def __init__(self, logger : logging.Logger, import_dir : str) -> None:
        self._import_directory = import_dir
        self._logger = logger.getChild(__name__)

    def gather(self) -> dict:
        """
        Walk the docoment root and create a dictionary of any files that are
        valid, along with it's name gennerate a hash.q

        returns:
            Returns a dictionary, where the key is path and the value is a list
            of tuples containning filename, hash and scan time.
        """
        files_list = {}

        for subdir, _, files in os.walk(self._import_directory):
            files_list[subdir] = []

            for file in files:
                filename = os.path.join(subdir, file)
                type_enum = self._determine_file_type(filename)

                if type_enum != file_type.FileType.UNKNOWN:
                    file_hash = self._generate_file_hash(filename)
                    just_file_ = filename.replace(self.import_directory, "")
                    self._logger.info(("File Gatherer found : '%s' "
                                       "| type: %s | hash: '%s'"),
                                       just_file_, type_enum.name, file_hash)
                    scan_time = int(round(time.time() * 1000))
                    entry = (file, file_hash, scan_time, type_enum)
                    files_list[subdir].append(entry)

            if not files_list[subdir]:
                del files_list[subdir]

        return files_list

    def _generate_file_hash(self, filename : str) -> str:
        # pylint: disable=no-self-use

        md5_object = hashlib.md5()
        block_size = 128 * md5_object.block_size

        with open(filename, 'rb') as file_handle:
            chunk = file_handle.read(block_size)
            while chunk:
                md5_object.update(chunk)
                chunk = file_handle.read(block_size)

        return md5_object.hexdigest()

    def _determine_file_type(self, filename : str) -> file_type.FileType:
        type_enum = file_type.FileType.UNKNOWN

        try:
            with open(filename, "r+", encoding="utf-8") as _:
                magic_file_type = magic.from_file(filename)
                type_enum = file_type.FileType.UNKNOWN

                if magic_file_type.startswith(self.FILETYPE_PDF):
                    type_enum = file_type.FileType.PDF

                elif magic_file_type.startswith(self.FILETYPE_TEXT):
                    type_enum = file_type.FileType.TEXT

                elif magic_file_type.startswith(self.FILETYPE_WORD):
                    type_enum = file_type.FileType.WORD

        except IOError:
            pass

        return type_enum

# Configure logging.
logger = logging.getLogger(__name__)
log_format= logging.Formatter("%(asctime)s [%(levelname)s] %(message)s",
                              "%Y-%m-%d %H:%M:%S")
console_stream = logging.StreamHandler()
console_stream.setFormatter(log_format)
logger.addHandler(console_stream)
logger.setLevel("DEBUG")

fg = FileGatherer(logger, "./import")
print(fg.gather())
