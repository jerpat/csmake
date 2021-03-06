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
from CsmakeModules.Packager import Packager
import os
import os.path
import email.Utils  #For RFC 2822 timestamp
import gzip
import sys
import subprocess
import StringIO
import tarfile
import hashlib

class DebianPackage(Packager):
    """Purpose: To create a .deb package that can be consumed by dpkg.
       Implements: Packager
       Type: Module   Library: csmake (core)
       Phases:
           package - Will build a debian package
           clean, package_clean - will delete the package
       Options:
           Common keywords:
               package-version - the version for the package
               maps - points to installmap based sections that
                      define how files should be mapped into the package
               result - directory to put the results
                        The package will be called
                             <name>-<version>-<package-version>.deb
               debian-directory-copyrignt= ID of a copyright section to use
                                           as the copyright for the debian
                                           information in the deb.
               arch - (OPTIONAL) Specify the architecture
                         amd64, i386 probably, or (default) all
               priority - (OPTIONAL) In debian, priority can be:
                   required, important, standard, optional, extra
                   (defaults to extra)
                   http://www.debian.org/doc/debian-policy/ch-archive.html#s-prioritiesalue ))
               signer - (OPTIONAL) Will create a _gpgorigin using the given
                        signer section.

       Joinpoints introduced:  See Packager module

       Flowcontrol Advice introduced:  See Packager module

       Install Map Definitions:  See Packager module
    """

    REQUIRED_OPTIONS = ['package-version', 'maps', 'result', 'debian-directory-copyright']

    METAMAP_METHODS = {
        'Package' : Packager.MetadataMapper,
        'Maintainer' : Packager.MetadataMapper,
        'Description' : Packager.MetadataMapper,
        'Depends' : Packager.MetadataMapper,
        'Recommends' : Packager.MetadataMapper,
        'Suggests' : Packager.MetadataMapper,
        'Enhances' : Packager.MetadataMapper,
        'Pre-depends' : Packager.MetadataMapper,
        'Breaks' : Packager.MetadataMapper,
        'Conflicts' : Packager.MetadataMapper,
        'Provides' : Packager.MetadataMapper,
        'Replaces' : Packager.MetadataMapper,
        'Section' : Packager.ClassifierMapper,
        '**python-lib' : Packager.AppendingClassifierMapper
    }

    METAMAP = {
        'Package' : 'name',
        'Maintainer' : 'packager',
        'Description' : 'description',
        'Depends' : 'depends',
        'Recommends' : 'recommends',
        'Suggests' : 'suggests',
        'Enhances' : 'enhances',
        'Pre-depends' : 'pre-depends',
        'Breaks' : 'breaks',
        'Conflicts' : 'conflicts',
        'Provides' : 'provides',
        'Replaces' : 'replaces'
    }

    #TODO: Probably would like it to be more elaborate
    # resulting tuple is (priority, seciton).
    # Lower priority (higher number) is less likely to be picked
    # (or less specific if you prefer)
    CLASSIFIER_MAPS = {
        'Section' : {
            '' :
                        (sys.maxint, 'misc'),
            'Intended Audience :: Developers' :
                        (9, 'devel'),
            'Topic :: Software Development :: Libraries' :
                        (5, 'libs'),
            'Topic :: Software Development :: Libraries :: Python Modules' :
                        (1, 'python'),
            'Programming Language :: Java' :
                        (1, 'java')
        },
        '**python-lib' : Packager.CLASSIFIER_MAPS['**python-lib']
    }

    #Find licensing here: https://spdx.org/licenses/
    #See CLDSYS-16651
    LICENSE_TEXTS = {
        'LGPL-2.1' : """ This library is free software; you can redistribute it and/or modify it under
 the terms of the GNU Lesser General Public License as published by the Free
 Software Foundation; version 2.1 of the License.
 .
 This library is distributed in the hope that it will be useful, but WITHOUT ANY
 WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
 PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.
 .
 You should have received a copy of the GNU Lesser General Public License along
 with this library; if not, write to the Free Software Foundation, Inc., 51
 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

On Debian systems, the complete text of the GNU Lesser General Public License
can be found in /usr/share/common-licenses/LGPL-2.1 file.""",

    }

    def _map_path_python_lib(self, value, pathmaps, pathkeymaps):
        Packager._map_path_python_lib(self, value, pathmaps, pathkeymaps)
        pathmaps[value] = \
            [ os.path.join(m, 'dist-packages') for m in pathmaps[value] ]
        pathkeymaps['python-lib'] = pathmaps[value]

    def _map_path_root(self, value, pathmaps, pathkeymaps):
        pathmaps[value] = ['.']
        self.archiveRoot = '.'
        pathkeymaps['root'] = [self.archiveRoot]

    def _createControlFileInfo(self, control, script=False):
        result = tarfile.TarInfo("./%s" % control)
        result.uid = 0
        result.uname = 'root'
        result.gid = 0
        result.gname = 'root'
        result.mode = 0644
        result.mtime = self._getCurrentPOSIXTime()

        if script:
            result.mode = result.mode | 0111
        return result

    def _writeMaintainerScript(self, script, control):
        maintfile = StringIO.StringIO()
        if 'text' in control:
            maintfile.write('\n'.join(control['text']))
        info = self._createControlFileInfo(script, True)
        self._addFileObjToControl(maintfile, info)
        maintfile.close()

    def _writeMaintainerFile(self, filetext, control):
        maintfile = StringIO.StringIO()
        if 'text' in control:
            maintfile.write('\n'.join(control['text']))
        info = self._createControlFileInfo(filetext, False)
        self._addFileObjToControl(maintfile, info)
        maintfile.close()

    def _control_prerm(self, control):
        self._writeMaintainerScript('prerm', control)

    def _control_postrm(self, control):
        self._writeMaintainerScript('postrm', control)

    def _control_preinst(self, control):
        self._writeMaintainerScript('preinst', control)

    def _control_postinst(self, control):
        self._writeMaintainerScript('postinst', control)

    def _control_shlibs(self, control):
        self._writeMaintainerFile('shlibs', control)

    def _control_control(self, control):
        controlfile = StringIO.StringIO()
        #TODO: Set order?
        for key, value in control.iteritems():
            if key.startswith('**'):
                continue
            controlfile.write('%s: %s\n' % (
                key,
                value ) )
        info = self._createControlFileInfo('control')
        self._addFileObjToControl(controlfile, info)
        controlfile.close()

    def _control_changelog(self, control):
        changelogfile = StringIO.StringIO()
        gzipper = gzip.GzipFile(mode='wb', fileobj=changelogfile, mtime=0)

        changelogPath = os.path.join(
            'usr/share/doc',
            self.packageMetadata['Package'],
            'changelog.Debian.gz' )

        #TODO: Fix this - it just writes the default for now
        gzipper.write(control['default-top'])
        gzipper.close()

        info = self._createArchiveFileInfo(changelogPath)
        info.uid = 0
        info.uname = 'root'
        info.gid = 0
        info.gname = 'root'
        info.mode = 0644
        self._addFileObjToArchive(changelogfile, info)
        changelogfile.close()

    def _writeCopyright(self, copyrightFile, copyright, path):
        self.log.devdebug("copyright to write for (%s) is : %s", path, str(copyright))
        if path is not None:
            copyrightFile.write(
                "Files: %s\n" % path )
        copyrightFile.write(
            "Copyright: %s %s\n" % (
                copyright['years'],
                copyright['holder'] ) )
        license = copyright['license'].strip()
        copyrightFile.write(
            "License: %s\n" % license)
        if license in DebianPackage.LICENSE_TEXTS:
            copyrightFile.write(DebianPackage.LICENSE_TEXTS[license])
            copyrightFile.write('\n')
        if 'disclaimer' in copyright:
            copyrightFile.write(
                "Disclaimer: %s\n" % copyright['disclaimer'] )
        copyrightFile.write('\n')

    #Can't do _control_md5sums, because there is no guaranteed ordering
    def _writeMD5sums(self, control):
        md5file = StringIO.StringIO()
        md5lines = control['entries']
        md5file.write('\n'.join(md5lines))
        md5file.write('\n')
        info = self._createControlFileInfo('md5sums')
        self._addFileObjToControl(md5file, info)
        md5file.close()

    def _control_copyright(self, control):
        copyrightFile = StringIO.StringIO()
        copyrightKeys = control['keys'].keys()
        initialKeyOrder = ['Format-Specification', 'Name', 'Maintainer']
        for key in initialKeyOrder:
            copyrightFile.write("%s: %s\n" % (
                key,
                control['keys'][key] ) )
            copyrightKeys.remove(key)
        for key in copyrightKeys:
            copyrightFile.write("%s: %s\n" % (
                key,
                control['keys'][key] ) )
        copyrightFile.write('\n')
        if 'default' in control:
            if type(control['default']) != list:
                defaults = [control['default']]
            else:
                defaults = control['default']
            for default in defaults:
                self._writeCopyright(
                    copyrightFile,
                    default,
                    None )

            for default in defaults:
                self._writeCopyright(
                    copyrightFile,
                    default,
                    '*' )

        copyrightPath = os.path.join(
            'usr/share/doc',
            self.packageMetadata['Package'],
            'copyright' )

        for key, value in control['files'].iteritems():
            self._writeCopyright(
                copyrightFile,
                value,
                key )

        info = self._createArchiveFileInfo(copyrightPath)
        info.uid = 0
        info.uname = 'root'
        info.gid = 0
        info.gname = 'root'
        info.mode = 0644
        self._addFileObjToArchive(copyrightFile, info)

    def _addFileObjToControl(self, fileobj, info):
        self._ensureArchivePath(self.controlfile, info)
        info.size = self._filesize(fileobj)
        fileobj.seek(0)
        self._filePlacingInPackage('control',None,info.name,fileobj)
        self.controlfile.addfile(info, fileobj)

    def _addInfoToControl(self, info):
        self._filePlacingInPackage('control',None,info.name,None)
        self.controlfile.addfile(info)

    def _doMetadataMappings(self):
        if 'arch' in self.options:
            self.arch = self.options['arch']
        else:
            self.arch = 'all'
        if 'priority' in self.options:
            priority = self.options['priority']
        else:
            priority = 'extra'
        Packager._doMetadataMappings(self) #Calls _calculateFileNameAndVersioning
        if 'Description' in self.packageMetadata \
            and 'about' in self.productMetadata:
            self.packageMetadata['Description'] += "\n %s" %'\n '.join(self.productMetadata['about'].replace('\n\n','\n.\n').split('\n'))
        self.packageName = self.packageMetadata['Package']
        self.packageMetadata['Version'] = self.fullVersion
        self.packageMetadata['Architecture'] = self.arch
        self.packageMetadata['Priority'] = priority
        self.packageMetadata['Urgency'] = 'low'  #This will be set by changelog

        control = self._packageControl('control')
        control.update(self.packageMetadata)

        copyright = self._packageControl('copyright')
        copyright['keys'] = {}
        copyright['keys']['Format-Specification'] = 'http://svn.debian.org/wsvn/dep/web/deps/dep5.mdwn?op=file&rev=135'
        copyright['keys']['Name'] = self.packageName
        copyright['keys']['Maintainer'] = self.packageMetadata['Maintainer']

        #Spits out a default changelog.  Use the DebianChangeLog
        #  aspect to get a resonable log.
        LOG="""%s (%s) %s; urgency=%s

%s

 -- %s  %s

"""
        changelog = self._packageControl('changelog')
        changelog['default-top'] = \
            LOG % (
                self.packageName,
                self.fullVersion,
                "experimental",
                "low",
                "  * Initial release",
                self.packageMetadata['Maintainer'],
                email.Utils.formatdate() )

        return self.packageMetadata

    def _calculateFileNameAndVersioning(self):
        #self.version = self.metadata._getDefaultDefinedVersion('+')
        self.format = 'gzip'
        Packager._calculateFileNameAndVersioning(self)
        self.version = self.metadata._getVersionWithFormat(
            [ "%(epoch)s:","%(primary)s" ],
            True,
            ['epoch', 'primary'],
            '+' )
        version = self.version
        self.filenameVersion = self.metadata._getVersionWithFormat(
            ["%(primary)s"],
            True,
            ['epoch', 'primary'],
            '+' )
        self.packageVersion = self.options['package-version']
        self.filenameFullVersion = '%s-%s' % (
            self.filenameVersion,
            self.packageVersion )
        self.fullVersion = '%s-%s' % (
            version,
            self.packageVersion )
        self.fullPackageName = '%s_%s_%s.deb' % (
            self.packageName,
            self.filenameFullVersion,
            self.arch )

    def _setupArchive(self):
        self.fullPathToArchive = os.path.join(
            self.resultdir,
            'data.tar.gz' )
        self._ensureDirectoryExists(self.resultdir, True)
        self.archive = tarfile.open(self.fullPathToArchive, 'w:gz')

    def _filePlacingInPackage(self, archive, sourcePath, archivePath, contents=None):
        Packager._filePlacingInPackage(self, archive, sourcePath, archivePath, contents)
        #Only md5 what's going in to the actual data archive
        if archive != 'data':
            return
        if sourcePath is not None:
            if os.path.isdir(sourcePath):
                self.log.devdebug("Adding directory: %s", sourcePath)
                return
            with open(sourcePath) as content:
                md5sum = self._fileMD5(content)
        elif contents is not None:
            if type(contents) == str:
                md5calc = hashlib.md5()
                md5calc.update(contents)
                md5sum = md5calc.hexdigest()
            else:
                md5sum = self._fileMD5(contents)
        else:
            self.log.warning("Neither sourcePath or contents were usable")
            return
        self.log.devdebug("Adding md5sum: %s   %s", md5sum, archivePath)
        self._packageControl('md5sums')['entries'].append(
            "%s  %s" % (
                md5sum,
                archivePath ) )

    def _setupPackage(self):
        Packager._setupPackage(self)
        self._ensureDirectoryExists(self.resultdir, True)
        md5sumsControl = self._packageControl('md5sums')
        md5sumsControl['entries'] = []
        with open(
            os.path.join(
                self.resultdir,
                'debian-binary' ), 'w' ) as dbfile:
            dbfile.write('2.0\n')
        self.fullPathToControl = os.path.join(
            self.resultdir,
            'control.tar.gz' )
        self.controlfile = tarfile.open(self.fullPathToControl, 'w:gz')

    def _finishPackage(self):
        #Write any remaining information
        result = Packager._finishPackage(self)
        self._writeMD5sums(self._packageControl('md5sums'))
        if result:
            #close control archive
            self.controlfile.close()
            filelist = [
                'debian-binary',
                'control.tar.gz',
                'data.tar.gz' ]
            if 'signer' in self.options:
                idname = self.options['signer']
                phase = self.engine.getPhase()
                signerResult = self.engine.launchStep(idname, phase)
                if signerResult is None or not signerResult._didPass():
                    raise ValueError("%s step failed" % idname)
                signer = signerResult._getReturnValue(phase)
                for f in filelist:
                    with open(os.path.join(self.resultdir, f)) as target:
                        buf = target.read(10240)
                        while len(buf) > 0:
                            signer.update(buf)
                            buf = target.read(10240)
                with open(os.path.join(self.resultdir, '_gpgorigin'), 'w') as g:
                    g.write(signer.digest())
                filelist.append('_gpgorigin')
            command = ['ar', 'rcv', self.fullPackageName] + filelist
            result = subprocess.call(
                command,
                stdout=self.log.out(),
                stderr=self.log.err(),
                cwd=self.resultdir )
            result = result == 0
        return result


