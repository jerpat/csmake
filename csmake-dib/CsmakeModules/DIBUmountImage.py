from CsmakeModules.DIBMountImage import DIBMountImage
import os
import os.path

class DIBUmountImage(DIBMountImage):
    """Purpose: Unmount the DIB Image for use/copy, etc
                DIBInit, DIBPrepDisk, and DIBMountImage
                should have been completed
                successfully before executing this section
       Phases:
           build 
       Flags:
           none
    """

    def build(self, options):

        dibenv = self.env.env['__DIBEnv__']
        mountpath = os.path.join(
            dibenv['build-dir'],
            'mnt' )
        statresult = os.statvfs(mountpath)
        if statresult is not None:
            #Populate the yielded files with extra information
            if self.yieldsfiles is not None:
                usedsize =  (statresult.f_frsize * statresult.f_blocks) \
                                   - (statresult.f_bsize * statresult.f_bfree)
                self.yieldsfiles[0]['used-size'] = usedsize
        return DIBMountImage.clean(self, options)
