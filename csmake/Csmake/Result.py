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
import StringIO
import pickle
import sys
import json
import traceback

class Result:

    LOG_DEBUG=400
    LOG_INFO=300
    LOG_WARNING=200
    LOG_ERROR=100
    LOG_QUIET=0

    def __init__(self, env, resultInfo={}):
        self.nesting = 0
        self.childResults = []
        self.resultType='Step'
        self.env = env
        self.settings = env.settings
        self.loglevel=Result.LOG_WARNING
        self.devoutput = self.settings['dev-output']
        if self.settings['debug']:
            self.loglevel=Result.LOG_DEBUG
        elif self.settings['verbose']:
            self.loglevel=Result.LOG_INFO
        elif self.settings['quiet']:
            self.loglevel=Result.LOG_QUIET
        self.chatter = not self.settings['no-chatter']
        self.params = resultInfo.copy()
        if 'status' not in self.params:
            self.params['status'] = "Unexecuted"
        if 'exception' not in self.params:
            self.params['exception'] = False
        self.outstream = StringIO.StringIO()
        if 'Out' not in self.params:
            self.params['Out'] = sys.stdout
        if 'Err' not in self.params:
            self.params['Err'] = self.params['Out']
        if 'Type' not in self.params:
            self.params['Type'] = '<<Type Unset>>'
        if 'Id' not in self.params:
            self.params['Id'] = '<<Step Id Unset>>'

        self.NESTNOTE='+'

        self.OUTPUT_HEADER="%s  %%s  %s\n" % ('-'*15, '-'*15)
        self.PASS_BANNER= "nununununununununununun"
        self.FAIL_BANNER= ".:*~*:._.:*~*:._.:*~*:."
        self.SKIP_BANNER= "- - - - - - - - - - - -"
        self.UNEX_BANNER= "                       "
        self.STATUS_FORMAT=" {1}   {2}: {3}   {1}\n"
        self.ANNOUNCE_FORMAT="{0} {1}@{2}      ---  {3}\n" 
        self.ONEXIT_ANNOUNCE_FORMAT="  /   {3} - Exit Handler: {0}@{1}  {2}\n"

        self.OBJECT_HEADER= \
"""
__________________________________________________________________
  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (
------------------------------------------------------------------"""
        self.OBJECT_FOOTER= \
"""__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)



"""
        self.ONEXIT_HEADER= \
"""
   ......................................................................
"""
        self.ONEXIT_FOOTER= \
""" ````````````````````````````````````````````````````````````````````````

"""

        self.ASPECT_JOINPOINT_HEADER="""
    ___________________________________________________
    \  Begin Joinpoint: %s    
     ```````````````````````````````````````````````````
"""
        self.ASPECT_JOINPOINT_FOOTER="""
     __________________________________________________
    /  End Joinpoint: %s
    ``````````````````````````````````````````````````
"""
        self.STATUS_SEPARATOR="%s\n" % ("-" * 66)
        self.ONEXIT_BEGIN_SEPARATOR=" %s\n" % ("`" *72)
        self.ONEXIT_END_SEPARATOR="   %s\n" % ("." * 70)

    def setTargetModule(self, targetModule):
        self.params['targetModule'] = targetModule

    def getTargetModule(self):
        if 'targetModule' in self.params:
            return self.params['targetModule']
        else:
            return None

    def forceQuiet(self):
        self.loglevel=Result.LOG_QUIET

    def setReturnValue(self, returnValue, key=None):
        if 'returnValue' not in self.params:
            self.params['returnValue'] = {}
        if key is None:
            key = "r__%d" % len(self.params['returnValue'])
        if key in self.params['returnValue']:
            newkey = "%s__%d" %(
                key,
                len(self.params['returnValue']) )
            self.params['returnValue'][newkey] = self.params['returnValue'][key]
        self.params['returnValue'][key] = returnValue

    def getReturnValues(self):
        if 'returnValue' in self.params:
            return self.params['returnValue']
        else:
            return None

    def getReturnValue(self, key):
        if 'returnValue' in self.params:
            if key in self.params['returnValue']:
                return self.params['returnValue'][key]
        return None

    def didPass(self):
        passed = True
        for result in self.childResults:
            passed = passed and not result.didFail()
        status = self.params['status']
        return passed \
             and (status == 'Passed' or status == 'Skipped')

    def didFail(self):
        failed = False
        for result in self.childResults:
            failed = failed or result.didFail()
        return failed or self.params['status'] == 'Failed' \
                      or self.params['status'] == 'Unexecuted'

    def unexecuted(self):
        self.params['status'] = 'Unexecuted'

    def passed(self):
        self.params['status'] = 'Passed'

    def failed(self):
        self.params['status'] = 'Failed'

    def skipped(self):
        self.params['status'] = 'Skipped'

    def executing(self):
        self.params['status'] = 'Executing'

    def err(self):
        result = self.params['Err']
        result.flush()
        return self.params['Err']

    def out(self):
        result = self.params['Out']
        result.flush()
        return self.params['Out']

    def appendChild(self, child):
        self.childResults.append(child)

    def write(self, output):
        self.outstream.write(output)
        if self.outstream is not self.params['Out']:
            self.params['Out'].write(output)

    def __repr__(self):
        reprResult = ['<<RESULT>> %s:%s: %s' % (
            self.params['Type'],
            self.params['Id'],
            self.params['status'] ) ]

        if self.params['status'] == 'Passed' or self.params['status'] == 'Failed':
           reprResult.append(Result.OUTPUT_HEADER % 'Step Output')
           reprResult.append(self.outstream.getvalue())
        return ''.join(reprResult)

    def __str__(self):
        return self.__repr__()

    def chatStart(self, nesting=0):
        self.nesting = nesting
        if self.loglevel:
            self.out() #Hack to flush
            if self.chatter:
                self.write(self.OBJECT_HEADER)
                self.write('\n')
                #TODO: revise all the chats to use a dict with format
                #       and to have an overridable format string
                # E.g., {key:s} the dict should be the params + ephemeral data
                self.write(self.ANNOUNCE_FORMAT.format(
                    self.NESTNOTE * self.nesting,
                    self.params['Type'],
                    self.params['Id'],
                    "Begin" ))
                self.write(self.STATUS_SEPARATOR)
            else:
                self.write(self.ANNOUNCE_FORMAT.format(
                    self.NESTNOTE * self.nesting,
                    self.params['Type'],
                    self.params['Id'],
                    "Begin" ))

    def chatStartOnExitCallback(self, name):
        if self.loglevel and self.chatter:
            self.out()
            self.write(self.ONEXIT_HEADER)
            self.write(self.ONEXIT_ANNOUNCE_FORMAT.format(
                self.params['Type'],
                self.params["Id"],
                name,
                "Begin" ))
            self.write(self.ONEXIT_BEGIN_SEPARATOR)

    def chatStartJoinPoint(self, joinpoint):
        self.currentjoinpoint = joinpoint
        if self.loglevel and self.chatter:
            self.out() #Hack to flush
            self.write(self.ASPECT_JOINPOINT_HEADER % joinpoint)
            self.write('\n')

    def chatEndJoinPoint(self):
        joinpoint = self.currentjoinpoint
        self.currentjoinpoint = None
        if self.loglevel and self.chatter:
            self.out() #Hack to flush
            self.write('\n')
            self.write(self.ASPECT_JOINPOINT_FOOTER % joinpoint)
            self.write('\n')

    def chatEndOnExitCallback(self, name):
        if self.loglevel and self.chatter:
            self.out()
            self.write(self.ONEXIT_END_SEPARATOR)
            self.write(self.ONEXIT_ANNOUNCE_FORMAT.format(
                self.params['Type'],
                self.params["Id"],
                name,
                "End" ))
            self.write(self.ONEXIT_FOOTER)

    def chat(self, output, cr=True):
        if self.loglevel:
            self.out() #Hack to flush
            self.write(output)
            if cr:
                self.write('\n')

    def chatStatus(self):
        if self.loglevel:
            self.out() #Hack to flush
            if self.chatter:
                self.write('\n')
                self.write(self.STATUS_SEPARATOR)
                if self.params['status'] == 'Passed':
                    statusBanner=self.PASS_BANNER
                elif self.params['status'] == 'Failed':
                    statusBanner=self.FAIL_BANNER
                elif self.params['status'] == 'Skipped':
                    statusBanner=self.SKIP_BANNER
                else:
                    statusBanner=self.UNEX_BANNER
                self.write(self.STATUS_FORMAT.format(
                    self.NESTNOTE * self.nesting,
                    statusBanner,
                    self.resultType,
                    self.params['status']) )
            else:
                self.write('\n%s Step Status: %s\n' % (
                    self.NESTNOTE * self.nesting,
                    self.params['status'] ) )

    def chatEnd(self):
        if self.loglevel:
            self.out() #Hack to flush
            if self.chatter:
                self.write(self.STATUS_SEPARATOR)
                self.write(self.ANNOUNCE_FORMAT.format(
                    self.NESTNOTE * self.nesting,
                    self.params['Type'],
                    self.params['Id'],
                    "End" ))
                self.write(self.STATUS_SEPARATOR)
                self.write(self.OBJECT_FOOTER)
            else:
                self.write(self.ANNOUNCE_FORMAT.format(
                    self.NESTNOTE * self.nesting,
                    self.params['Type'],
                    self.params['Id'],
                    "End" ))

    def repeatOutput(self, fobj, nesting=0):
        if not self.loglevel:
            fobj.write(self.OBJECT_HEADER)
            fobj.write("%s %s@%s               Begin\n" %(
                self.NESTNOTE * nesting,
                self.params['Type'],
                self.params['Id'] ))
            fobj.write("\n")
            fobj.write(self.outstream.getvalue())
            fobj.write("\n")
            fobj.write(self.STATUS_SEPARATOR)
            if self.params['status'] == 'Passed':
                statusBanner=self.PASS_BANNER
            elif self.params['status'] == 'Failed':
                statusBanner=self.FAIL_BANNER
            else:
                statusBanner=self.UNEX_BANNER
            fobj.write(self.STATUS_FORMAT.format(
                "+" * nesting,
                statusBanner,
                self.resultType,
                self.params['status'],
                statusBanner ) )
            
            fobj.write(self.OBJECT_FOOTER)
        else:
            fobj.write(self.outstream.getvalue())

    def picklePrint(self, fobj):
        parts = fobj.params.clone()
        parts['Out'] = self.outstream.getvalue()
        del parts['Err']
        pickle.dump(parts, fobj)

    def jsonPrint(self, fobj):
        parts = fobj.params.clone()
        parts['Out'] = self.outstream.getvalue()
        del parts['Err']
        json.dump(parts, fobj)

    def log(self, level, output, *params):
        try:
            self.write("%s@%s: %s: %s\n" % (
                self.params['Type'],
                self.params['Id'],
                level,
                output % params ) )
        except:
            self.write('%%%s@%s: %s: %s %s\n' % (
            self.params['Type'],
            self.params['Id'],
            level,
            output,
            str(params) ))

    def info(self, output, *params):
        if self.loglevel >= Result.LOG_INFO:
            self.log('INFO     ', output, *params)

    def exception(self, output, *params):
        ei = sys.exc_info()
        if self.loglevel >= Result.LOG_DEBUG or self.devoutput:
            sio = StringIO.StringIO()
            traceback.print_exception(ei[0], ei[1], ei[2], None, sio)
            s = sio.getvalue()
            sio.close()
            if s[-1:] == "\n":
                s = s[:-1]
            self.log("EXCEPTION", "%s\n%s" %(
                output % params,
                s ))
        elif self.loglevel >= Result.LOG_ERROR:
            self.log("EXCEPTION", output, *params) 
            self.log("EXCEPTION", "%s: %s\n" % (
                str(ei[0].__name__), 
                str(ei[1]).strip("'").strip('"')))

    def error(self, output, *params):
        if self.loglevel >= Result.LOG_ERROR:
            self.log("ERROR    ", output, *params)

    def warning(self, output, *params):
        if self.loglevel >= Result.LOG_WARNING:
            self.log("WARNING  ", output, *params)

    def notice(self, output, *params):
        if self.loglevel >= Result.LOG_WARNING:
            self.log("NOTICE  ", output, *params)

    def critical(self, output, *params):
        self.log("*CRITICAL", output, *params)

    def debug(self, output, *params):
        if self.loglevel >= Result.LOG_DEBUG:
            self.log("DEBUG    ", output, *params)

    def devdebug(self, output, *params):
        if self.devoutput:
            self.log("^%^%^ DEV", output, *params)
