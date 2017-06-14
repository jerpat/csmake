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
