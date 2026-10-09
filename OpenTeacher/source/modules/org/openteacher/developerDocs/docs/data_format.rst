===========
Data format
===========

All data types are described in Python objects. (dicts, unicode strings,
bools, datetime, lists, etc.)

.. contents:: `Contents:`

list
====

generic
-------
::

	{
		#All optional (empty allowed too)
		"items": [],
		"tests": [],
	}

words
-----
::

	{
		#All optional. Strings may be empty alternatively too.
		"title": u"Test",
		"questionLanguage": u"Nederlands",
		"answerLanguage": u"English",
		"created": datetime.datetime.now(),
	}

item
====

generic
-------
::

	{
		#required
		"id": 0, #an integer unique in this list
	}

words
-----
::

	#everything (except the id) is optional.

	#Input: in {+acc (2x)} = 1. in, op 2. tijdens
	#or: in = 1. in, op 2. tijdens {+acc (2x)}
	word1 = {
		"id": 0,
		"questions": [
			[u"in"],
		],
		"answers": [
			[u"in",	u"op"],
			[u"tijdens"],
		],
		"comment": u"+acc (2x)",
		"commentAfterAnswering": u"You knew that one, right?",
		"created": datetime.datetime.now(),
	}

	#Input: in {+abl (2x)} = 1. naar(binnen), in 2. tot, jegens
	word2 = {
		"id": 1,
		"questions": [
			[u"in"],
		],
		"answers": [
			[u"naar(binnen)", u"in"],
			[u"tot", u"jegens"],
		],
		"comment": u"+abl (2x)",
		"created": datetime.datetime.now(),
	}

topo
----
::

	#all required
	{
		"id": 0,
		"name": u"Leeuwarden",
		"x": 20, #non-negative int
		"y": 50, #non-negative int
	}

media
-----
::

	#all required
	{
		"id": 0,
		"remote": True,
		"name": u"",
		"filename": u"",
		"question": u"",
		"answer": u"",
	}

test
====
::

	{
		#every key is optional
		"finished": True,
		"results": [], #may be empty too
		"pauses": [],
	}

result
======

generic
-------
::

	{
		#required entries
		"result": u"right", #or u"wrong"
		"itemId": 0, #the id of an item

		#optional entry
		"active": {
			"start": datetime.datetime(),
			"end": datetime.datetime(),
		},
	}

words
-----
::

	{
		"result": "right", #right, wrong, or another value *if really necessary*

		#optional
		"givenAnswer": u"one",

		#inherited
		"itemId": 0,
		"active": {
			"start": datetime.datetime.now(),
			"end": datetime.datetime.now(),
		},
	}

	#&

	{
		"result": "wrong",
		"itemId": 1,
		"givenAnswer": u"twoo",
		"active": {
			"start": datetime.datetime.now(),
			"end": datetime.datetime.now(),
		},
	}

pauses
======
::

	#all required
	{
		"start": datetime.datetime.now(),
		"end": datetime.datetime.now(),
	}
