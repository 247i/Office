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

from django.db import models
from django.contrib.auth.models import User, Group

class UserProfile(models.Model):
	user = models.OneToOneField(User)

	role = models.CharField(max_length=200)

class Test(models.Model):
	teacher = models.ForeignKey(User, related_name="teacher")
	list = models.TextField()
	
	class Meta(object):
		permissions = (
			('do_test', "Do test"),
		)

class Answers(models.Model):
	test = models.ForeignKey(Test)
	student = models.ForeignKey(User)
	list = models.TextField()

	class Meta(object):
		unique_together = ("test", "student")

	def __unicode__(self):
		return "Answers of '%s'" % self.student.username

class CheckedAnswers(models.Model):
	answer = models.ForeignKey(Answers, unique=True)
	list = models.TextField()
	note = models.CharField(max_length=200, blank=True)
