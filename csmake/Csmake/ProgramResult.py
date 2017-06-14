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
from Result import Result
from phases import phases

class ProgramResult(Result):

    def __init__(self, env, version, resultInfo={}):
        Result.__init__(self, env, resultInfo)
        self.OBJECT_HEADER="""
 ___  ______  ______  ______  ______  ______  ______  ______  ______  ___
  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__
 (______)(______)(______)(______)(______)(______)(______)(______)(______)
"""
        self.OBJECT_FOOTER=self.OBJECT_HEADER
        self.PASS_BANNER="""
  .--.      .--.      .--.      .--.      .--.      .--.      .--.      .
:::::.\\::::::::.\\::::::::.\\::::::::.\\::::::::.\\::::::::.\\::::::::.\\::::::
'      `--'      `--'      `--'      `--'      `--'      `--'      `--'
"""
        self.FAIL_BANNER="""
  __   __   __   __   __   __   __   __   __   __   __   __   __   __   __
 _\/_ _\/_ _\/_ _\/_ _\/_ _\/_ _\/_ _\/_ _\/_ _\/_ _\/_ _\/_ _\/_ _\/_ _\/_
 \/\/ \/\/ \/\/ \/\/ \/\/ \/\/ \/\/ \/\/ \/\/ \/\/ \/\/ \/\/ \/\/ \/\/ \/\/
"""
        self.STATUS_FORMAT="""{1}
     {2}: {3}
"""
        self.ANNOUNCE_FORMAT="""
     {3} csmake - version %s
""" % version
        self.resultType="csmake"

        self.PHASE_BANNER="""       _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _
    ,-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)
    `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-'
"""

    def log(self, level, output, *params):
        #print "XXX Output: %s" % output
        #print "XXX params: %s" % str(params)
        try:
            self.write("` %s: %s\n" % (
                level,
                output % params ) )
        except:
            self.write("  %s: %s(%s)" % (
                str(level),
                str(output),
                str(params) ) )

    def chatStartPhase(self, phase, doc=None):
        if self.loglevel:
            if self.chatter:
                self.write(self.PHASE_BANNER)
            self.write("         BEGINNING PHASE: %s\n" % phase)
            if doc is not None:
                self.write("             %s\n" % doc)

    def chatEndPhase(self, phase, doc=None):
        if self.loglevel:
            self.write("\n         ENDING PHASE: %s\n" % phase)
            if doc is not None:
                self.write("             %s\n" % doc)

    def chatEndLastPhaseBanner(self):
        if self.loglevel and self.chatter:
            self.write(self.PHASE_BANNER)

    def chatEndSequence(self, sequence, doc=None):
        if self.loglevel:
            if len(sequence) > 0:
                self.write("\n   SEQUENCE EXECUTED: %s\n" % phases.joinSequence(
                                                                sequence) )
                if doc is not None:
                    self.write("     %s\n" % doc)
