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
