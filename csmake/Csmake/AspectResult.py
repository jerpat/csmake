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

class AspectResult(Result):

    def __init__(self, env, resultInfo={}):
        Result.__init__(self, env, resultInfo)
        if 'cuts' not in self.params:
            self.params['cuts'] = '<<Cut Type Unset>>'
        if 'AspectId' not in self.params:
            self.params['AspectId'] = '<<No Aspect Id>>'
        self.PASS_BANNER="      ~~~~~~      "
        self.FAIL_BANNER="      ######      "
        self.NESTNODE="      &"
        self.nesting=1
        self.resultType='Aspect'
        self.OBJECT_HEADER="""       _________________________________________
      |--               Aspect                --|
       \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        ``````````````````````````````````````````"""

        self.STATUS_SEPARATOR="        ------------------------------------------\n"
        self.OBJECT_FOOTER="""        _________________________________________
       //////////////////////////////////////////
      |--             End Aspect              --|
       ``````````````````````````````````````````
"""
        self.STATUS_FORMAT="{0}   {1} {2}: {3} {1}\n"
        self.ANNOUNCE_FORMAT="        &{1}@{2}         ...  {3}\n"

    #TODO: Join points with multiple advisements are getting success/fail/skip
    #      Status overwritten.

    def log(self, level, output, *params):
        try:
            self.write("        &%s@(%s): %s: %s\n" % (
                self.params['Type'],
                self.params['cuts'],
                level,
                output % params ) )
        except:
            self.write("        &%s@(%s): %s: %s (%s)\n" % (
                self.params['Type'],
                self.params['cuts'],
                level,
                output,
                params ) )
