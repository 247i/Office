#	Copyright 2011, Marten de Vries
#
#	This file is part of OpenTeacher.
#
#	OpenTeacher is free software: you can redistribute it and/or modify
#	it under the terms of the GNU Affero General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	OpenTeacher is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU Affero General Public License for more details.
#
#	You should have received a copy of the GNU Affero General Public License
#	along with OpenTeacher.  If not, see <http://www.gnu.org/licenses/>.

from django import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from models import User, Group, Answers

import json

def isValidRole(role):
	if role not in ("admin", "teacher", "student"):
		raise ValidationError("Invalid role, must be 'admin', 'teacher' or 'student'.")

def isStudent(user):
	try:
		if user.get_profile().role == "student":
			return #everything fine
	except (AttributeError, ObjectDoesNotExist):
		pass #something wrong
	raise ValidationError("The chosen user isn't a student")

def isValidJson(data):
	try:
		json.loads(data)
	except Exception:
		raise ValidationError("Unable to parse the json, is it valid?")

class UsersForm(forms.Form):
	username = forms.CharField(max_length=200)
	password = forms.CharField(max_length=200, widget=forms.PasswordInput)
	role = forms.CharField(max_length=200, validators=[isValidRole], required=False, help_text='Only changes made by admins are persistent.')

class GroupsForm(forms.Form):
	name = forms.CharField(max_length=200)

class GroupForm(forms.Form):
	student_id = forms.ModelChoiceField(User.objects.all(), validators=[isStudent])

class TestsForm(forms.Form):
	list = forms.CharField(widget=forms.Textarea, validators=[isValidJson])

class TestGroupsForm(forms.Form):
	group_id = forms.ModelChoiceField(Group.objects.all())

class TestStudentsForm(forms.Form):
	student_id = forms.ModelChoiceField(User.objects.all(), validators=[isStudent])

class TestAnswersForm(forms.Form):
	list = forms.CharField(widget=forms.Textarea, validators=[isValidJson])

class TestCheckedAnswerForm(forms.Form):
	list = forms.CharField(widget=forms.Textarea, validators=[isValidJson])
	note = forms.CharField()

class TestCheckedAnswersForm(TestCheckedAnswerForm):
	answer_id = forms.ModelChoiceField(Answers.objects.all(), help_text="Choose an answer from the current test")
