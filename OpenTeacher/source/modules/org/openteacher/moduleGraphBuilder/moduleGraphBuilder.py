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

#pyratemp is imported in enable()

class ModuleGraphBuilderModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(ModuleGraphBuilderModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "moduleGraphBuilder"

		self.requires = (
			self._mm.mods(type="qtApp"),
			self._mm.mods(type="metadata"),
		)

	def _addEdges(self, mod, graph, demands, color):
		for demand in demands:
			for demandedMod in demand:
				graph.add_edge(mod.type, demandedMod.type, dir="forward", color=color)

	def buildModuleGraph(self, path):
		graph = pygraphviz.AGraph(**{
			"label": "%s module map" % self._metadata["name"],
			"labelloc": "t", #top
			"fontsize": len(set(self._mm.mods)) * 1.25,
			"fontname": "Ubuntu",
			"strict": False,
		})
		graph.node_attr["style"] = "filled"

		hue = self._metadata["mainColorHue"]
		color = unicode(QtGui.QColor.fromHsv(hue, 41, 250).name())
		graph.node_attr["fillcolor"] = color
		for mod in self._mm.mods:
			if not hasattr(mod, "type"):
				continue
			graph.add_node(mod.type)
			if hasattr(mod, "requires"):
				self._addEdges(mod, graph, mod.requires, "#555555")
			if hasattr(mod, "uses"):
				self._addEdges(mod, graph, mod.uses, "#dddddd")

		graph.draw(path, prog="dot")

	def enable(self):
		global pygraphviz, QtGui
		try:
			import pygraphviz
			from PyQt4 import QtGui
		except ImportError:
			return #remaining inactive

		self._modules = set(self._mm.mods(type="modules")).pop()
		self._metadata = self._modules.default("active", type="metadata").metadata

		self.active = True

	def disable(self):
		self.active = False

		del self._modules
		del self._metadata

def init(moduleManager):
	return ModuleGraphBuilderModule(moduleManager)
