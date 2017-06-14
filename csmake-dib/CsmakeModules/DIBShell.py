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
from CsmakeModules.Shell import Shell
import os
import subprocess
import sys

class DIBShell(Shell):
    """Purpose: Execute out to a shell command in a DIB environment
       Flags:
           command - shell command to execute (semi-colons need to be escaped)
             use command(<phase>) to specify the command for a given phase
             default is 'build'
           env - Reference to a ShellEnv to use
                 Can be multiple envs, comma separated
                 These environment definitions will be used in conjunction
                 with the current DIB environment.
       Phase: Any
       Example:
           [ShellEnv@my-command-env]
           THIS_DIR=mydir

           [DIBShell@my-command]
           command = mkdir -p ${THIS_DIR} && pushd ${THIS_DIR} 
              ifconfig > my.cfg 
              ls
              popd
              ls
           env = my-command-env, default-env"""

    def _getStartingEnvironment(self, options):
        if '__DIBEnv__' in self.env.env:
            self.dibenv = self.env.env['__DIBEnv__']
            self.newenv = self.dibenv['shellenv']
            return self.newenv
        else:
            return Shell._getStartingEnvironment(self, options)
