#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011, Milan Boers
#	Copyright 2011-2012, Marten de Vries
#	Copyright 2009, Dennis Hofs
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

#The comments describing the file format are taken from Voca's source
#code. For that, Dennis Hofs is mentioned in the copyright section of
#this file (licenses of both projects match). The comments came from the
#following files:
#
#- WordListSerialiserImpl40.cs
#- SerialiserFactoryImpl40.cs
#- SerialiserFactoryImpl30.cs
#- GrammarSerialiser.cs
#- EmbeddedFileSerialiser.cs
#- ViewStateSerialiserImpl40.cs
#- WordListSerialiserImpl10.cs
#- SerialiserFactoryImpl10.cs
#- CharsetEncodings.cs

import struct
import collections
import itertools

class Reader(object):
	def __init__(self, data, *args, **kwargs):
		super(Reader, self).__init__(*args, **kwargs)

		self._data = data
		self._pos = 0

	@property
	def atEnd(self):
		return self._pos == len(self._data)

	def skip(self, fmt):
		size = struct.calcsize(fmt)
		self._pos += size

	def read(self, fmt):
		startPos = self._pos
		self.skip(fmt)

		return struct.unpack(fmt, self._data[startPos:self._pos])[0]

	readInt = lambda self: self.read(">i")
	readChar = lambda self: self.read(">b")
	readUnsignedChar = lambda self: self.read(">B")
	readLongLong = lambda self: self.read(">q")
	readBool = lambda self: self.read(">?")
	readBytes = lambda self, length: self.read(">%ss" % length)

	skipInt = lambda self: self.skip(">i")
	skipChar = lambda self: self.skip(">b")
	skipBool = lambda self: self.skip(">?")
	skipBytes = lambda self, length: self.skip(">%ss" % length)

class VocaLoaderModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(VocaLoaderModule, self).__init__(*args, **kwargs)

		self.type = "load"
		self.priorities = {
			"default": 432,
		}
		self._mm = moduleManager
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.requires = (
			self._mm.mods(type="wordsStringParser"),
			self._mm.mods(type="mimicryTypefaceConverter"),
		)
		self.filesWithTranslations = ("voca.py",)

	@property
	def _convertMimicryTypeface(self):
		return self._modules.default("active", type="mimicryTypefaceConverter").convert

	@property
	def _parse(self):
		return self._modules.default("active", type="wordsStringParser").parse

	def _retranslate(self):
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)
		#TRANSLATORS: This is one of the file formats OpenTeacher
		#TRANSLATORS: can read. It's named after the program that uses
		#TRANSLATORS: it. See http://www.oriente-voca.eu/ for more info
		#TRANSLATORS: on it.
		self.name = _("Voca")

	def enable(self):
		self.loads = {"wdl": ["words"]}
		self.mimetype = "application/x-oriente-voca"

		self._modules = set(self._mm.mods(type="modules")).pop()
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.active = True

	def disable(self):
		self.active = False

		del self.name
		del self.loads
		del self.mimetype

		del self._modules
		if hasattr(self, "_reader"): # pragma: no cover
			del self._reader

	def getFileTypeOf(self, path):
		if path.endswith(".wdl"):
			return "words"

	def _readUtf8String(self):
		size = self._reader.readInt()
		return unicode(self._reader.readBytes(size), encoding="UTF-8")

	def _skipUtf8String(self):
		size = self._reader.readInt()
		self._reader.skipBytes(size)

	def _readLang(self):
		#this is found directly after the header
		#(name + version numbers)
		#note this function only parses one of the two blocks at once.
		#
		# 4 foreign language name size (int)
		# * foreign language name (UTF-8 string)
		# 4 foreign font name size (int)
		# * foreign font name (UTF-8 string)
		# 4 foreign font size
		#
		# 4 reference language name size (int)
		# * reference language name (UTF-8 string)
		# 4 reference font name size (int)
		# * reference font name (UTF-8 string)
		# 4 reference font size

		lang = self._readUtf8String()
		font = self._readUtf8String()
		self._reader.skipInt()

		return (lang, font)

	def _skipGrammar(self):
		# 4 grammar item count (int)
		# (
		itemCount = self._reader.readInt()
		for i in xrange(itemCount):
			# 4 category size (int)
			# * category (UTF-8 string)
			# 4 value size (int)
			# * value (UTF-8 string)
			for i in xrange(2):
				self._skipUtf8String()
		# )*

	def _skipEmbeddedFile(self):
		# (
		#	 (file path is an empty string)
		#	 8 [ 0 ] (long)
		# |
		#	 (file path is not an empty string)
		#	 8 file size (long)
		#	 4 extension size (int)
		#	 * extension (UTF-8 string)
		#	 * file data (bytes with length of file size)
		# )
		fileSize = self._reader.readLongLong()
		if fileSize:
			self._skipUtf8String()
			self._reader.skipBytes(fileSize)

	def _readLangs(self, list):
		answerLanguage, answerFont = self._readLang()
		questionLanguage, questionFont = self._readLang()

		list["questionLanguage"] = questionLanguage
		list["answerLanguage"] = answerLanguage

		return (questionFont, answerFont)

	def _skipHeader(self):
		#0xA is the header length
		self._reader.skipBytes(0xA)

	def _skipPhoneticAndForeignChars(self):
		# 4 phonetic font name size (int)
		# * phonetic font name (UTF-8 string)
		# 4 phonetic font size
		# 
		# 4 foreign characters size (int)
		# * foreign characters (UTF-8 string)

		#skip it all
		self._skipUtf8String()
		self._reader.skipInt()
		self._skipUtf8String()

	def _skipPartOfSpeech(self):
		# 4 part of speech count (int)
		# (
		#		4 part of speech size (int)
		#		* part of speech (UTF-8 string)
		#		4 grammar category count (int)
		#		(
		#			4 grammar category size (int)
		#			* grammar category (UTF-8 string)
		#		)*
		#	)*

		#skip it all. Bit harder this time.
		partOfSpeechCount = self._reader.readInt()
		for i in xrange(partOfSpeechCount):
			self._skipUtf8String()
			grammarCategoryCount = self._reader.readInt()
			for i in xrange(grammarCategoryCount):
				self._skipUtf8String()

	def _skipUploaded(self):
		# 1 uploaded (bool)
		# (
		#     (if uploaded)
		#     4 upload name size (int)
		#     * upload name (UTF-8 string)
		#     1 has foreign language ISO code (bool)
		#     (
		#         (if has foreign language ISO code)
		#         3 foreign language ISO code (char[])
		#     )?
		#     1 has reference language ISO code (bool)
		#     (
		#         (if has reference language ISO code)
		#         3 reference language ISO code (char[])
		#     )?
		#     4 course size (int)
		#     * course (UTF-8 string)
		#     4 comments size (int)
		#     * comments (UTF-8 string)
		# )?

		#skip it all. Starting to be annoying...
		uploaded = self._reader.readBool()
		if uploaded:
			self._skipUtf8String()
			for i in xrange(2):
				hasLanguageIsoCode = self._reader.readBool()
				if hasLanguageIsoCode:
					self._reader.skipBytes(3)
			for i in xrange(2):
				self._skipUtf8String()

	def _skip40OnlyExerciseInfo(self):
		# 4 mastered score (1-10) (int)
		# 4 maximum mastered chance (0 for 0%, 100 for 100%) (int)
		# 4 exam count (int)

		#skip all
		for i in xrange(3):
			self._reader.skipInt()

	def _skipCommonExerciseInfo(self):
		# 4 active exercise type (int)
		# 4 exercise type count (int)
		# (
		self._reader.skipInt()

		exerciseTypeCount = self._reader.readInt()
		for i in xrange(exerciseTypeCount):
			# (
			# 	1 false
			# 	4 exercise type name size (int)
			# 	* exercise type name (UTF-8 string)
			# )
			# |
			# (
			# 	1 true
			# 	4 size of language pack path to exercise type name (int)
			# 	* language pack path to exercise type name (UTF-8 string)
			# )

			#skip it
			self._reader.skipBool()
			self._skipUtf8String()

			# 4 answer type size (int)
			# * answer type (UTF-8 string)
			# 4 exercise configuration count (int)
			# (
			self._skipUtf8String()
			exerciseConfigCount = self._reader.readInt()
			for i in xrange(exerciseConfigCount):
				# (
				# 	1 false
				# 	4 exercise configuration name size (int)
				# 	* exercise configuration name (UTF-8 string)
				# )
				# |
				# (
				# 	1 true
				# 	4 size of language pack path to exercise configuration name (int)
				# 	* language pack path to exercise configuration name (UTF-8 string)
				# )
				self._reader.skipBool()
				self._skipUtf8String()

				# 4 question field count (int)
				# (
				# 	4 question field size (int)
				# 	* question field (UTF-8 string)
				# )*
				# 4 answer field count (int)
				# (
				# 	1 check answer field (bool)
				# 	4 answer field size (int)
				# 	* answer field (UTF-8 string)
				# )*
				# 4 info field count (int)
				# (
				# 	4 info field size (int)
				# 	* info field (UTF-8 string)
				# )*
				questionFieldCount = self._reader.readInt()
				for i in xrange(questionFieldCount):
					self._skipUtf8String()
				answerFieldCount = self._reader.readInt()
				for i in xrange(answerFieldCount):
					self._reader.skipBool()
					self._skipUtf8String()
				infoFieldCount = self._reader.readInt()
				for i in xrange(infoFieldCount):
					self._skipUtf8String()
			# )*
		# )*

	def _readItems(self, list, questionFont, answerFont, loadImages):
		#Finally. Some interesting stuff again.
		# 4 item count (int)
		# (
		itemCount = self._reader.readInt()
		for wordId in xrange(itemCount):
			# 4 sequence (int)
			# 4 word size (int)
			# * word (UTF-8 string)
			# 1 word score (byte)
			# 4 word trans size (int)
			# * word trans (UTF-8 string)
			# 1 word trans score (byte)
			# 4 context size (int)
			# * context (UTF-8 string)
			# 1 context score (byte)
			# 4 phonetic size (int)
			# * phonetic (UTF-8 string)
			# 1 phonetic score (byte)
			# 4 part of speech size (int)
			# * part of speech (UTF-8 string)
			# * grammar (see GrammarSerialiser)
			# 1 grammar score (byte)
			# * media (see EmbeddedFileSerialiser)
			# 1 media score (byte)
			# * image (see EmbeddedFileSerialiser) -- ATTENTION: This is 4.0 only
			# 1 image score (byte) -- ATTENTION: This is 4.0 only
			# 4 lesson size (int)
			# * lesson (UTF-8 string)
			# 4 page size (int)
			# S* page (UTF-8 string)
			self._reader.skipInt()
			answer = self._readUtf8String()
			self._reader.skipChar()
			question = self._readUtf8String()
			self._reader.skipChar()

			for i in xrange(2):
				self._skipUtf8String()
				self._reader.skipChar()
			self._skipUtf8String()
			self._skipGrammar()
			self._reader.skipChar()
			self._skipEmbeddedFile()
			self._reader.skipChar()
			if loadImages:
				self._skipEmbeddedFile()
				self._reader.skipChar()

			for i in xrange(2):
				self._skipUtf8String()

			#convert mimicry font symbols
			question = self._convertMimicryTypeface(questionFont, question)
			answer = self._convertMimicryTypeface(answerFont, answer)

			list["items"].append({
				"id": wordId,
				"questions": self._parse(question),
				"answers": self._parse(answer),
			})
		# )*

	def _parse40(self):
		list = {
			"items": [],
			"resources": [],
		}

		self._skipHeader()
		questionFont, answerFont = self._readLangs(list)
		self._skipPhoneticAndForeignChars()
		self._skipPartOfSpeech()
		self._skipUploaded()
		self._skip40OnlyExerciseInfo()
		self._skipCommonExerciseInfo()
		self._readItems(list, questionFont, answerFont, loadImages=True)

		#We've got all the interesting stuff by now. Just in case I
		#missed something, the remaining part of the file format
		#description:

		# Reads or writes a global view state in the following format:
		# 
		# 1 mode (MainForm.Mode)
		# 1 apply filters (bool)
		# 4 filter count (int)
		# (
		#	 1 filter class (0 = StringFilter,
		#					1 = BooleanFilter,
		#					2 = StringListFilter)
		#	 4 type size (int)
		#	 * type (UTF-8 string)
		#	 (
		#		 (StringFilter)
		#		 1 search type (StringFilter.SearchTypes)
		#		 4 string size (int)
		#		 * string (UTF-8 string)
		#	 |
		#		 (BooleanFilter)
		#		 1 converter type (0 = EmbeddedFileBooleanConverter)
		#		 1 value (bool)
		#	 |
		#		 (StringListFilter)
		#		 4 string count (int)
		#		 (
		#			 4 string size (int)
		#			 * string (UTF-8 string)
		#		 )*
		#	 )
		# )*
		# 4 applied filter count (int)
		# (
		#	 4 string size (int)
		#	 * applied filter type (UTF-8 string)
		# )*
		# 4 unsatisfied filter count (int)
		# (
		#	 4 string size (int)
		#	 * unsatisfied filter type (UTF-8 string)
		# )*
		# 4 dirty indices count (int)
		# (
		#	 4 dirty index (int)
		# )*
		# 4 column count (int)
		# (
		#	 4 type size
		#	 * type (UTF-8 string)
		#	 1 visible (bool)
		#	 4 width (int)
		# )*
		# 1 selection type (Selection.SelectionType)
		# (
		#	 (CellSelection)
		#	 4 row (int)
		#	 4 column (int)
		# |
		#	 (RowSelection)
		#	 4 first row (int)
		#	 4 last row (int)
		# )?
		# 4 top row (int)
		# 4 left column (int)
		# 1 has editor view state (bool)
		# (
		#	 1 editor view state class (0 = DefaultViewState, 1 = TextViewState)
		#	 (
		#		 (TextViewState)
		#		 4 selection start (int)
		#		 4 selection length (int)
		#	 )?
		# )?
		# (
		#	 1 input language set (bool)
		#	 (
		#		 (if input language set)
		#		 4 culture size (int)
		#		 * culture (UTF-8 string)
		#		 4 layout size (int)
		#		 * layout (UTF-8 string)
		#	 )?
		# ){3} (for input modes: foreign, reference, phonetic)

		return list

	def _parse30(self):
		list = {
			"items": [],
			"resources": [],
		}

		self._skipHeader()
		questionFont, answerFont = self._readLangs(list)
		self._skipPhoneticAndForeignChars()
		self._skipPartOfSpeech()
		self._skipUploaded()
		self._skipCommonExerciseInfo()
		self._readItems(list, questionFont, answerFont, loadImages=False)

		return list

	def _readNullTerminatedString(self):
		string = ""
		while True:
			char = self._reader.readUnsignedChar()
			if not char:
				break
			string += chr(char)
		return string

	def _skipNullTerminatedString(self):
		while True:
			char = self._reader.readUnsignedChar()
			if not char:
				break

	def _parse10(self):
		list = {
			"items": [],
			"resources": [],
		}

		# 22 [ 2E F6 26 4F 25 BD 2C 59 03 8F 59 AA 1E 34 46 07 6C 4A 44 CF 28 00 ]
		bytes = self._reader.readBytes(22)
		#check magic id
		assert(bytes.encode("hex") == "2ef6264f25bd2c59038f59aa1e3446076c4a44cf2800")

		# * foreign language (null-terminated string)
		# 1 foreign font charset (charset)
		# * foreign font name (null-terminated string)
		# 1 foreign font size (byte)
		# * reference language (null-terminated string)
		# 1 reference font charset (charset)
		# * reference font name (null-terminated string)
		# 1 reference font size (byte)
		answerLang = self._readNullTerminatedString()
		answerEncoding = self._readCharset()
		list["answerLanguage"] = unicode(answerLang, encoding=answerEncoding)
		answerFont = self._readNullTerminatedString()
		self._reader.skipChar()

		questionLang = self._readNullTerminatedString()
		questionEncoding = self._readCharset()
		list["questionLanguage"] = unicode(questionLang, encoding=questionEncoding)
		questionFont = self._readNullTerminatedString()
		self._reader.skipChar()

		# * foreign characters (null-terminated string)
		self._skipNullTerminatedString()

		# 2 [ 0D 00 ]
		bytes = self._reader.readBytes(2)
		assert(bytes.encode("hex") == "0d00")

		# The format of a list of items is as follows. The end of the list
		# should correspond to the end of the stream.
		# 
		# (
		# 	* word (null-terminated string)
		# 	* word trans (null-terminated string)
		# 	* context (null-terminated string)
		# 	* part of speech (null-terminated string)
		# 	* lesson (null-terminated string)
		# 	4 sound size (int)
		# 	* sound (bytes)
		# 	1 foreign to reference set (exercise level)
		# 	1 reference to foreign set (exercise level)
		# 	1 foreign to reference progress (byte, max 30)
		# 	1 reference to foreign progress (byte, max 30)
		# 	1 foreign to reference asked (byte, max 5)
		# 	1 reference to foreign asked (byte, max 5)
		# 	1 foreign to reference score (byte, 5 low order bits are answers to last questions)
		# 	1 reference to foreign score (byte, 5 low order bits are answers to last questions)
		# 	2 [ 0D 00 ]
		# )*
		counter = itertools.count()
		while not self._reader.atEnd:
			answer = unicode(self._readNullTerminatedString(), encoding=answerEncoding)
			question = unicode(self._readNullTerminatedString(), encoding=questionEncoding)
			for i in range(3):
				self._skipNullTerminatedString()
			soundSize = self._reader.readInt()
			self._reader.skipBytes(soundSize)
			self._reader.skipBytes(8)

			bytes = self._reader.readBytes(2)
			assert(bytes.encode("hex") == "0d00")

			#convert mimicry typeface chars into unicode
			question = self._convertMimicryTypeface(questionFont, question)
			answer = self._convertMimicryTypeface(answerFont, answer)

			list["items"].append({
				"id": next(counter),
				"questions": self._parse(question),
				"answers": self._parse(answer),
			})

		return list

	def _readCharset(self):
		#public const byte ANSI_CHARSET = 0;
		#public const byte DEFAULT_CHARSET = 1;
		#public const byte SHIFTJIS_CHARSET = 128;
		#public const byte HANGEUL_CHARSET = 129;
		#public const byte GB2312_CHARSET = 134;
		#public const byte CHINESEBIG5_CHARSET = 136;
		#public const byte JOHAB_CHARSET = 130;
		#public const byte HEBREW_CHARSET = 177;
		#public const byte ARABIC_CHARSET = 178;
		#public const byte GREEK_CHARSET = 161;
		#public const byte TURKISH_CHARSET = 162;
		#public const byte VIETNAMESE_CHARSET = 163;
		#public const byte THAI_CHARSET = 222;
		#public const byte EASTEUROPE_CHARSET = 238;
		#public const byte RUSSIAN_CHARSET = 204;
		#public const byte BALTIC_CHARSET = 186;

		#case DEFAULT_CHARSET:
		#case ANSI_CHARSET:
		#	return Encoding.GetEncoding("windows-1252");
		#case EASTEUROPE_CHARSET:
		#	return Encoding.GetEncoding("windows-1250");
		#case BALTIC_CHARSET:
		#	return Encoding.GetEncoding("windows-1257");
		#case RUSSIAN_CHARSET:
		#	return Encoding.GetEncoding("windows-1251");
		#case GREEK_CHARSET:
		#	return Encoding.GetEncoding("windows-1253");
		#case TURKISH_CHARSET:
		#	return Encoding.GetEncoding("windows-1254");
		#case ARABIC_CHARSET:
		#	return Encoding.GetEncoding("windows-1256");
		#case HEBREW_CHARSET:
		#	return Encoding.GetEncoding("windows-1255");
		#case THAI_CHARSET:
		#	return Encoding.GetEncoding("windows-874");
		#case VIETNAMESE_CHARSET:
		#	return Encoding.GetEncoding("windows-1258");
		#case GB2312_CHARSET:
		#	return Encoding.GetEncoding("gb2312");
		#case CHINESEBIG5_CHARSET:
		#	return Encoding.GetEncoding("big5");
		#case SHIFTJIS_CHARSET:
		#	return Encoding.GetEncoding("shift_jis");
		#case HANGEUL_CHARSET:
		#	return Encoding.GetEncoding("ks_c_5601-1987");
		#case JOHAB_CHARSET:
		#	return Encoding.GetEncoding("Johab");
		#default:
		#	return Encoding.GetEncoding("windows-1252");

		code = self._reader.readUnsignedChar()
		return {
			0: "windows-1252",
			1: "windows-1252",
			128: "shift_jis",
			129: "ks_c_5601-1987",
			134: "gb2312",
			136: "big5",
			130: "Johab",
			177: "windows-1255",
			178: "windows-1256",
			161: "windows-1253",
			162: "windows-1254",
			163: "windows-1258",
			222: "windows-874",
			238: "windows-1250",
			204: "windows-1251",
			186: "windows-1257",
		}[code]

	def load(self, path):
		with open(path, "rb") as f:
			data = f.read()

		#header:
		#
		# 8 VOCAWRDL
		# 1 major version (4)
		# 1 minor version (0)
		FileStart = collections.namedtuple("FileStart", "magicId majorVersion minorVersion")
		start = FileStart._make(struct.unpack(">8sBB", data[:0xA]))

		#used by _parse40() and _parse30() (and methods they call)
		self._reader = Reader(data)
		if start.magicId == "VOCAWRDL":
			if start.majorVersion == 4 and start.minorVersion == 0:
				list = self._parse40()
			elif start.majorVersion == 3 and start.minorVersion == 0:
				list = self._parse30()
			else: # pragma: no cover
				raise ValueError("Unknown file format version")
		else:
			#give vocatude a chance on reading the file
			list = self._parse10()

		return {
			"resources": {},
			"list": list,
		}

def init(moduleManager):
	return VocaLoaderModule(moduleManager)
