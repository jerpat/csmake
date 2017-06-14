from Csmake.CsmakeAspect import CsmakeAspect

class DIBRunPartsAspect(CsmakeAspect):
    """Purpose: To modify the run-dib-parts processing with a workaround.
                These aspects should only modify DIBRunParts steps
       Phases: *
       Joinpoints Added: script_skip, script_start, script_passed
                         script_failed, script_exception, script_end
       Flags:
           partOverride - the part(s) proposed for overriding, 
                          e.g. 01-install-selinx"""

    def _installPartHandler(self, options, stepoptions):
        self.override = options['partOverride']
        partName = "__%s" % self.override.strip()
        if partName not in stepoptions:
            stepoptions[partName] = []
        stepoptions[partName].append( (self,options) )

    def start(self, phase, options, step, stepoptions):
        self.options = options
        self._installPartHandler(options, stepoptions)
        self.log.passed()
    
