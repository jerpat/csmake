from CsmakeModules.ShellToEnvironment import ShellToEnvironment
import os

class DIBShellToEnvironment(ShellToEnvironment):
    """Purpose: Migrate Shell Variables to the environment
                Will access the DIB shell environment if one is available
                Puts a shell environment variable into the csmake environment
                This enables the ability to allow the DIB process
                to feed back to the build process
                - should be used with caution as this opens builds
                  up to depend on a specific shell/DIB context to work properly
                  which is antithetical to the theory of operation
                  behind csmake
                *Options substitutions, e.g., %(var)s, are NOT allowed*
       Library: cloudsystem-appliance-build
       Phases: build - ensures full definitions
               *any* - environment may
       Options: Adds all options into the environment for future steps
                The value is a shell variable that should have been
                defined before csmake was executed."""

    def _getStartingEnvironment(self):
        if '__DIBEnv__' in self.env.env:
            self.dibenv = self.env.env['__DIBEnv__']
            self.newenv = self.dibenv['shellenv']
            return self.newenv
        else:
            return os.environ

    def default(self, options):
        self.log.debug("Skipping actual execution of this step")
        for key in options.keys():
            self.env.env[key] = None
        self.log.passed()
        return True

    def build(self, options):
        savedEnviron = os.environ
        try:
            env = self._getStartingEnvironment()
            os.environ = env
            ShellToEnvironment.default(self, options)
        finally:
            os.environ = savedEnviron
        return True
