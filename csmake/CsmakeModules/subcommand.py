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
from CsmakeModules.command import command

class subcommand(command):
    """Purpose: Execute a series of build steps
                (Not intended to be directly executed from the command line)
       Implements: command
       Type: Module   Library: csmake (core)
       Phases: *any*
       Options: The keys are used to order the steps lexigraphically
                e.g.: 1, 10, 2, 20, 200, 3, A, a (suggestion use 0000-9999)
                The values are atomic groups of steps
                   , - denotes step follows the next
                   & - denotes steps that can be run in parallel
           description - provides a description (documentation) of what
                         the subcommand is supposed to accomplish.
       Example:
           [subcommand@some-common-steps]
           description = "Encapsulates all the steps"
           10 = repo1 & repo2 & repo3, repo4
           20 = createPond
           100 = final-step-not-really

           [command@build]
           description = "This will build a small pond"
           0000 = init
           0010 = some-common-steps
           0020 = stockFish

           In the example above, if 'build' is executed, then the sections
           would be performed as follows:
           First, an init section would be executed
           Then, the subcommand, 'some-common-steps' would be executed
                which would lead to the following steps executed in *this*
                order:
                    1) repo1, repo2, and repo3 would execute in parallel
                    2) repo4 would then be executed
                    3) *** final-step-not-really *** would execute next
                       NOTE: 100 comes before 20 lexicographically
                    4) createPond would execute last for the subcommand
           Finally, 'stockfish' would execute.
    """

    RESERVED_FLAGS = ['description']

    def __repr__(self):
        return "<<subcommand step definition>>"

    def __str__(self):
        return "<<subcommand step definition>>"


