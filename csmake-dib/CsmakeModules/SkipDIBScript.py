from CsmakeModules.DIBRunPartsAspect import DIBRunPartsAspect

class SkipDIBScript(DIBRunPartsAspect):
    """Purpose: To completely skip a specified script
       Phases: build
       Flags:
           partOverride - the script proposed for skipping, 
                          e.g. 01-install-selinx"""

    def script_start__build(self, phase, options, step, stepoptions):
        self.flowcontrol.override('doNotStartScript', True, self)
        self.log.passed()
        return True

