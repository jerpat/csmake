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
from CsmakeModules.DIBShell import DIBShell
from CsmakeModules.DIBRunPartsAspect import DIBRunPartsAspect
from CsmakeModules.ShellAspect import ShellAspect
import os
import subprocess
import sys

class DIBShellAspect(DIBRunPartsAspect, ShellAspect):
    """Purpose: Execute out to a shell command in a DIB environment
                on advice of a DIBRunParts step joinpoints 
               (or any CsmakeModule based step, actually)
       Flags:
           command(<point>)
              - shell command to execute (semi-colons need to be escaped)
                where <point> is either
                    command(<joinpoint>) or 
                    command(<joinpoint>__<phase>)
                    (just as any other aspect)
           advise(<point>[#<time>]) = <advise point>:<vote>
              - Will vote Yes or No on the given advice control point
                (only on commands implemented)
                <time> (optional) represents what it will do on the 
                       specified time the
                       the joinpoint specified is executed for the given step
                       If not used the same advice will be given every time
                <advise point> is the flow control point to advise on
                    (e.g., tryAgain)
                <vote> is either True or False
           env - Reference to a ShellEnv to use
                 Can be multiple envs, comma separated
                 These environment definitions will be used in conjunction
                 with the current DIB environment.
           exec - (Optional) Set the shell command (Default: /bin/bash)
       Phase: Any
       Joinpoint: Any
       Example:
           [ShellEnv@my-command-env]
           THIS_DIR=mydir

           [DIBRunParts@my-step]
           stuff=happens

           #This will shell on start of 05-some-stuff
           #  in the build phase
           [&DIBShellAspect@my-step doshellstuff]
           partOverride=05-some-stuff
           command(start_script__build) = 
              mkdir -p ${THIS_DIR} && pushd ${THIS_DIR} 
              ifconfig > my.cfg 
              ls
              popd
              ls
           env = my-command-env, default-env"""

    def __init__(self, env, log):
        DIBRunPartsAspect.__init__(self, env, log)
        ShellAspect.__init__(self, env, log)
        self.sheller = DIBShell(env, log)

    def _lookupSubclassImplementedJoinPoints(self, joinpoint, phase, options):
        return DIBRunPartsAspect._joinPointLookup(
            self, joinpoint, phase, options )

    def _joinPointLookup(self, joinpoint, phase, options):
        return ShellAspect._joinPointLookup(
            self, joinpoint, phase, options)
