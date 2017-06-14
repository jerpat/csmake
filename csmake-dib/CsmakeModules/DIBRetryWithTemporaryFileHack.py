# <copyright>
# (c) Copyright 2017 Hewlett Packard Enterprise Development LP
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# </copyright>
from CsmakeModules.DIBTemporaryFileHack import DIBTemporaryFileHack
import shutil
import os.path
import subprocess

class DIBRetryWithTemporaryFileHack(DIBTemporaryFileHack):
    """Purpose: Modify a file for a specific DIB step after it fails
                If multiple flags are defined the order of operation
                  is replace, replace-file, patch, patch-file, append,
                    then append-file
                If the path to the specified file does not exist
                  it will be created then deleted unless 'keepChanges'
                  is True
                The path to temp-file will not be created if it is different
                  and does not exist
                (Do not use the chrooted paths)
       Phases: build
       Flags:
           partOverride - the script proposed for skipping, 
                          e.g. 01-install-selinx
           file - File to modify
           temp-file - location to store the old file to restore it
              Default: <file dir>/<file name>.csmake-DIBTemporaryFileHack-save
           keepChanges - The old file will not be restored if True
                     The step actions will be skipped if the specified
                     temporary file exists.
           patch - Inline patch diff (not implemented yet)
           patch-file - File containing the patch diff to apply (not impl)
           replace - Inline replacement of the file
           replace-file - File containing the new version
           append - Inline append of the file 
           append-file - File containing the new lines to append (not impl)
    """

    def script_failed__build(self, phase, options, step, stepoptions):
        try:
            if not self.retried:
                self.retried = True
                self.log.info('Reattempting step')
                self.flowcontrol.override("tryScriptAgain", True, self)
                return DIBTemporaryFileHack.script_start__build(self, phase, options, step, stepoptions)
            else:
                self.log.info("Step failed on retry, punting")
                self.log.failed()
                return False
        except:
            self.log.devdebug("bases are: %s", str(self.__class__.__bases__))
            self.log.devdebug("class is: %s", repr(self.__class__))
            self.log.devdebug("DIBTemporaryFileHack is: %s", repr(DIBTemporaryFileHack))
            self.log.exception("Failed to hack file")
            self.log.failed()
            return False

    def script_start__build(self, phase, options, step, stepoptions):
        self.retried = False
        self.dirpath = None
        self.log.passed()
        return True

    def script_end__build(self, phase, options,step,stepoptions):
        if self.retried:
            return DIBTemporaryFileHack.script_end__build(self, phase, options, step, stepoptions)
        else:
            self.log.passed()
            return True
