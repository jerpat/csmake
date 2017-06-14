from Csmake.CsmakeModule import CsmakeModule
import subprocess

class DIBPackagePhasedImage(CsmakeModule):
    """Purpose: To package a partial DIB image
           A DIBInit and any DIBRepo steps should be run prior to executing
           this step.
       Phases: build, clean, archive
       Flags:
    """

    def build(self, options):
        dibenv = self.env.env['__DIBEnv__']

        result = subprocess.call(
            ['sudo', 'tar', '-czvf', dibenv['result-image'], '-C', dibenv['build-dir'], '.' ],
            stdout=self.log.out(),
            stderr=self.log.err())

        if result == 0:
            self.log.passed()
            return True
        else:
            self.log.failed()
            return False

    def clean(self, options):
        dibenv = self.env.env['__DIBEnv__']
        result = subprocess.call(
            ['sudo', 'rm', dibenv['result-image']],
            stdout=self.log.out(),
            stderr=self.log.err())
        self.log.passed()
        return True

    def archive(self, options):
        self.log.warning("archive:  NOT IMPLEMENTED YET")
        self.log.passed()
        return True
