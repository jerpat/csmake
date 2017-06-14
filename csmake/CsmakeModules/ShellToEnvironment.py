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
from Csmake.CsmakeModuleAllPhase import CsmakeModuleAllPhase
import os

class ShellToEnvironment(CsmakeModuleAllPhase):
    """Purpose: Puts a shell environment variable into the csmake environment
       Type: Module   Library: csmake (core)
       Description:
                This enables the ability to paramiterize a build
                - should be used with caution as this opens builds
                  up to depend on a specific shell context to work properly
                  which is antithetical to the theory of operation
                  behind csmake
                *Options substitutions, e.g., %(var)s, are NOT allowed*
       Phases: *any*
       Options: Adds all flags into the environment for future steps
                The value is a shell variable that should have been
                defined before csmake was executed.
       Example:
           [ShellToEnvironment@pull-parameters]
           csmake-build-number=BUILDNO
           branch-to-pull=BRANCH

           The 'pull-parameters' section would pull 'BUILDNO' from the
           shell enivronment that csmake is executing from and place it
           in the csmake environment variable called "csmake-build-number"
           Likewise with 'BRANCH', 'branch-to-pull' would be set to
           whatever ${BRANCH} would evaluate to from the shell that launched
           csmake.
    """

    def __repr__(self):
        return "<<ShellToEnvironment step definition>>"

    def __str__(self):
        return "<<ShellToEnvironment step definition>>"

    def _doOptionSubstitutions(self, stepdict):
        #Avoid options substitutions for this module
        pass

    def default(self, options):
        for option, shellkey in options.iteritems():
            if option.startswith("**"):
                continue
            if shellkey not in os.environ:
                self.log.error("'%s' was not defined in the shell environment", shellkey)
                self.log.failed()
                return False
            self.env.env[option] = os.environ[shellkey]
        self.log.passed()
        return True

