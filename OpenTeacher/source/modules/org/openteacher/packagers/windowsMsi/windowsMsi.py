#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2012, Marten de Vries
#
#	This file is part of OpenTeacher.
#
#	OpenTeacher is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	OpenTeacher is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with OpenTeacher.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import shutil
import uuid
import subprocess
import itertools

wxs = """
<?xml version="1.0" encoding="UTF-8" ?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
	<Product Name="{name}" Id="*" UpgradeCode="6fbe08a3-4545-45b8-b6d1-4eaf00083835" Language="1033" Codepage="1252" Version="3.0.0.1" Manufacturer="{name} Maintainers">
	<Package Id="*" Keywords="Installer" Manufacturer="{name} Maintainers" InstallerVersion="100" Languages="1033" Compressed="yes" />

	<!-- files -->
	<Media Id="1" Cabinet="{name}.cab" EmbedCab="yes" />
	<Directory Id="TARGETDIR" Name="SourceDir">
		<Directory Id="ProgramFilesFolder" Name="PFiles">
		<Directory Id="INSTALLDIR" Name="{name}">
			<Component Id="MainFiles" Guid="{uuid1}">
				<File Id="{lower_name}.exe" KeyPath="yes" Name="{lower_name}.exe" Source="{lower_name}.exe" DiskId="1">
					<Shortcut Id="StartmenuShortcut" Directory="ProgramMenuDir" Name="{name}" WorkingDirectory="INSTALLDIR" Icon="{lower_name}.exe" Advertise="yes" />
					<Shortcut Id="DesktopShortcut" Directory="DesktopFolder" Name="{name}" WorkingDirectory="INSTALLDIR" Icon="{lower_name}.exe" Advertise="yes" />
				</File>

				<!-- File associations -->
				{file_associations}
				<CreateFolder/>
			</Component>
			{files}
		</Directory>
		</Directory>
		<Directory Id="ProgramMenuFolder" Name="Programs">
		<Directory Id="ProgramMenuDir" Name="{name}">
			<Component Id="ProgramMenuDir" Guid="{uuid2}">
			<RemoveFolder Id="ProgramMenuDir" On="uninstall" />
			<RegistryValue Root="HKCU" Key="Software\[Manufacturer]\[ProductName]" Type="string" Value="" KeyPath="yes" /> 
			<!-- Uninstall shortcut -->
			<Shortcut Id="UninstallShortcut" Name="Uninstall {name}" Target="[SystemFolder]msiexec.exe" Arguments="/x [ProductCode]" Description="Uninstalls {name}" />
			<CreateFolder/>
			</Component>
		</Directory>
		</Directory>
		<Directory Id="DesktopFolder" Name="Desktop" />
	</Directory>
	<Feature Id="Complete" Level="1">
		<ComponentRef Id="MainFiles" />
		<ComponentRef Id="ProgramMenuDir" />
		{components}
	</Feature>

	<!-- UI -->
	<UI>
		<UIRef Id="WixUI_InstallDir" />
		<UIRef Id="WixUI_ErrorProgressText" />
		<Publish
		Dialog="ExitDialog"
		Control="Finish"
		Event="DoAction"
		Value="LaunchApplication"
		>WIXUI_EXITDIALOGOPTIONALCHECKBOX = 1 and NOT Installed</Publish>
	</UI>
	<Property Id="WIXUI_INSTALLDIR" Value="INSTALLDIR" />
	<WixVariable Id="WixUIBannerBmp" Value="topbanner.bmp" />
	<WixVariable Id="WixUIDialogBmp" Value="leftbanner.bmp" />
	<WixVariable Id="WixUILicenseRtf" Value="COPYING.rtf" />

	<!-- Launch after install -->
	<Property Id="WIXUI_EXITDIALOGOPTIONALCHECKBOXTEXT" Value="Launch {name}" />
	<Property Id="WixShellExecTarget" Value="[#{lower_name}.exe]" />
	<CustomAction Id="LaunchApplication" BinaryKey="WixCA" DllEntry="WixShellExec" Impersonate="yes" />

	<Property Id="ARPPRODUCTICON" Value="openteacher.exe" />
	<Icon Id="{lower_name}.exe" SourceFile="{lower_name}.exe" />
	</Product>
</Wix>
"""

class WindowsMsiPackagerModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(WindowsMsiPackagerModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "windowsMsiPackager"
		self.requires = (
			self._mm.mods(type="pyinstallerInterface"),
			self._mm.mods(type="execute"),
			self._mm.mods(type="metadata"),
		)
		self.uses = (
			self._mm.mods(type="load"),
		)
		self.priorities = {
			"package-windows-msi": 0,
			"default": -1,
		}

		self._ids = {}
		self._idCounter = itertools.count()

	def _toId(self, path):
		if path not in self._ids:
			self._ids[path] = "generated_%s" % next(self._idCounter)
		return self._ids[path]

	def _gatherFiles(self, root):
		"""gather all files in the python and src directories. Output as xml ready to insert into the main snippet"""

		components = '<ComponentRef Id="%sComponent" />' % self._toId(root)

		result = '<Directory Id="{id}Directory" Name="{name}">'.format(id=self._toId(root), name=os.path.basename(root))
		result += '<Component Id="{id}Component" Guid="{uuid}">'.format(id=self._toId(root), uuid=uuid.uuid4())

		for file in os.listdir(root):
			if root == "." and file in [self._metadata["name"].lower() + ".exe", "COPYING.rtf", "leftbanner.bmp", "topbanner.bmp"]:
				#added manually or not needed at runtime.
				continue
			if not os.path.isfile(os.path.join(root, file)):
				continue
			result += '<File Id="{id}" Source="{source}" Name="{name}" DiskId="1" />'.format(
				id=self._toId(os.path.join(root, file)),
				source=os.path.join(root, file),
				name=file,
			)
		result += '<CreateFolder/></Component>'
		for dir in os.listdir(root):
			if not os.path.isdir(os.path.join(root, dir)):
				continue
			components2, result2 = self._gatherFiles(os.path.join(root, dir))
			components += components2
			result += result2
		result += '</Directory>'
		return components, result

	def _run(self):
		try:
			msiLoc = sys.argv[1]
		except IndexError:
			sys.stderr.write("Please specify the resultive msi file name as last command line parameter. (e.g. AppName.msi)\n")
			return
		#build to exe, dll etc.
		resultDir = self._pyinstaller.build()

		#copying in files needed to create the msi.
		shutil.copy(
			self._mm.resourcePath("leftbanner.bmp"),
			os.path.join(resultDir, "leftbanner.bmp")
		)
		shutil.copy(
			self._mm.resourcePath("topbanner.bmp"),
			os.path.join(resultDir, "topbanner.bmp")
		)
		shutil.copy(
			self._mm.resourcePath("COPYING.rtf"),
			os.path.join(resultDir, "COPYING.rtf")
		)

		cwd = os.getcwd()
		os.chdir(resultDir)

		#complete the template and write it to the hard disk
		components, files = self._gatherFiles(".")

		fileAssociations = ""
		alreadyDone = set()
		for mod in self._modules.sort("active", type="load"):
			if not hasattr(mod, "mimetype"):
				continue
			for ext in mod.loads.keys():
				if ext in alreadyDone:
					continue
				alreadyDone.add(ext)
				fileAssociations += """\n
				<!-- .{ext}-->
 				<ProgId Id="{name}.{ext}" Description="{desc}" Icon="{lower_name}.exe">
					<Extension Id="{ext}" ContentType="{mimetype}">
						<Verb Id="open" Command="open" TargetFile="{lower_name}.exe" Argument="&quot;%1&quot;" />
					</Extension>
				</ProgId>""".format(
					name=self._metadata["name"],
					lower_name=self._metadata["name"].lower(),
					ext=ext,
					desc=mod.name,
					mimetype=mod.mimetype
				)

		with open("OpenTeacher.wxs", "wb") as f:
			f.write(wxs.strip().format(
				files=files,
				components=components,
				uuid1=uuid.uuid4(),
				uuid2=uuid.uuid4(),
				name=self._metadata["name"],
				lower_name=self._metadata["name"].lower(),
				file_associations=fileAssociations,
			))

		#build msi
		wixPath = os.path.join(os.environ["ProgramFiles"], "Windows Installer XML v3.5/bin/")

		subprocess.check_call(wixPath + "candle.exe OpenTeacher.wxs")
		subprocess.check_call(wixPath + "light.exe -ext WixUtilExtension -ext WixUIExtension OpenTeacher.wixobj")

		#switch back cwd
		os.chdir(cwd)

		#send back the result
		shutil.copy(
			os.path.join(resultDir, "OpenTeacher.msi"),
			msiLoc
		)

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		self._metadata = self._modules.default("active", type="metadata").metadata
		self._pyinstaller = self._modules.default("active", type="pyinstallerInterface")

		self._modules.default(type="execute").startRunning.handle(self._run)

		self.active = True

	def disable(self):
		self.active = False

		del self._modules
		del self._metadata
		del self._pyinstaller

def init(moduleManager):
	return WindowsMsiPackagerModule(moduleManager)
