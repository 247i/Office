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

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from django.core.urlresolvers import reverse

from djangorestframework.views import View
from djangorestframework.response import Response, ErrorResponse
from djangorestframework import status

from guardian.shortcuts import assign, remove_perm, get_users_with_perms, get_groups_with_perms

from models import Test, Answers, CheckedAnswers, User, UserProfile, Group
from forms import UsersForm, GroupsForm, GroupForm, TestsForm, TestGroupsForm, TestStudentsForm, TestAnswersForm, TestCheckedAnswersForm, TestCheckedAnswerForm

import json

def role(request):
	try:
		return request.user.get_profile().role
	except (AttributeError, ObjectDoesNotExist):
		if request.user.is_superuser:
			return "admin" #to give rights to the user installing...
		return None

class IndexView(View):
	def get(self, request):
		return {
			"name": "OpenTeacher test server",
			"version": "3.x",
			"urls": [
				reverse("users"),
				reverse("groups"),
				reverse("tests"),
			],
		}

class UsersView(View):
	form = UsersForm

	def get(self, request):
		results = []
		hasRights = role(request) in ("admin", "teacher")
		for user in User.objects.all():
			if hasRights or user == request.user:
				results.append({
					"id": user.id,
					"username": user.username,
					"url": reverse("user", kwargs={"id": user.id}),
				})
		return results

	def post(self, request):
		if role(request) == "admin":
			try:
				user = User.objects.create_user(**{
					"username": self.CONTENT["username"],
					"password": self.CONTENT["password"],
					"email": "",
				})
			except IntegrityError:
				return Response(status.HTTP_400_BAD_REQUEST, "Username already in use.")

			UserProfile.objects.create(**{
				"user": user,
				"role": self.CONTENT["role"],
			})
			return reverse("user", kwargs={"id": user.id})
		else:
			return Response(status.HTTP_401_UNAUTHORIZED)

class UserView(View):
	form = UsersForm

	def get(self, request, id):
		try:
			user = User.objects.get(id=id)
		except ObjectDoesNotExist:
			return Response(status.HTTP_404_NOT_FOUND)
		data = {
			"id": user.id,
			"username": user.username,
			"url": reverse("user", kwargs={"id": user.id}),
		}
		try:
			profile = user.get_profile()
		except ObjectDoesNotExist:
			pass
		else:
			data["role"] = profile.role
		return data

	def put(self, request, id):
		try:
			user = User.objects.get(id=id)
		except ObjectDoesNotExist:
			return Response(status.HTTP_404_NOT_FOUND)
		try:
			profile = user.get_profile()
		except ObjectDoesNotExist:
			#no one can change django superusers/anonymous users
			return Response(status.HTTP_401_UNAUTHORIZED)
		if role(request) == 'admin':
			profile.role = self.CONTENT["role"]
		if role(request) == "admin" or request.user == user:
			user.username = self.CONTENT["username"]
			user.set_password(self.CONTENT["password"])
			try:
				user.save()
			except IntegrityError:
				return Response(status.HTTP_400_BAD_REQUEST, "Username already in use.")
			profile.save()
			return reverse("user", kwargs={"id": id})
		else:
			return Response(status.HTTP_401_UNAUTHORIZED)

	def delete(self, request, id):
		if role(request) == "admin":
			try:
				User.objects.get(id=id).delete()
			except ObjectDoesNotExist:
				return Response(status.HTTP_404_NOT_FOUND)
			else:
				return reverse("users")
		else:
			return Response(status.HTTP_401_UNAUTHORIZED)

class UserMeView(View):
	def get(self, request):
		if role(request) is not None:
			return reverse("user", kwargs={"id": request.user.id})
		else:
			return Response(status.HTTP_401_UNAUTHORIZED)

class GroupsView(View):
	form = GroupsForm

	def get(self, request):
		groups = Group.objects.all()
		results = []
		for group in groups:
			results.append({
				"id": group.id,
				"name": group.name,
				"url": reverse("group", kwargs={"group_id": group.id}),
			})
		return results

	def post(self, request):
		if role(request) == "admin":
			try:
				group = Group.objects.create(name=self.CONTENT["name"])
			except IntegrityError:
				return Response(HTTP_400_BAD_REQUEST, "Group name already in use.")
			return reverse("group", kwargs={"group_id": group.id})
		else:
			return Response(status.HTTP_401_UNAUTHORIZED)

class GroupView(View):
	form = GroupForm

	def get(self, request, group_id):
		try:
			group = Group.objects.get(id=group_id)
		except ObjectDoesNotExist:
			return Response(status.HTTP_404_NOT_FOUND)
		students = User.objects.filter(groups=group)
		results = []
		for student in students:
			results.append(reverse("group_member", kwargs={
				"group_id": group_id,
				"student_id": student.id
			}))
		return {
			"name": group.name,
			"url": reverse("group", kwargs={"group_id": group_id}),
			"id": group_id,
			"members": results,
		}

	def post(self, request, group_id):
		try:
			group = Group.objects.get(id=group_id)
		except ObjectDoesNotExist:
			return Response(status.HTTP_404_NOT_FOUND)
		student = self.CONTENT["student_id"]

		if role(request) == "admin":
			student.groups.add(group)
			return reverse("group_member", kwargs={"group_id": group_id, "student_id": student.id})
		else:
			return Response(status.HTTP_401_UNAUTHORIZED)

	def delete(self, request, group_id):
		try:
			group = Group.objects.get(id=group_id)
		except ObjectDoesNotExist:
			return Response(status.HTTP_404_NOT_FOUND)
		if role(request) == "admin":
			group.delete()
			return reverse("groups")
		else:
			return Response(status.HTTP_401_UNAUTHORIZED)

class GroupMemberView(View):
	def get(self, request, group_id, student_id):
		return {
			"url": reverse("group_member", kwargs={"group_id": group_id, "student_id": student_id}),
			"user": reverse("user", kwargs={"id": student_id}),
			"group": reverse("group", kwargs={"group_id": group_id})
		}

	def delete(self, request, group_id, student_id):
		try:
			group = Group.objects.get(id=group_id)
		except ObjectDoesNotExist:
			return Response(status.HTTP_404_NOT_FOUND)
		try:
			user = User.objects.get(id=student_id)
		except ObjectDoesNotExist:
			return Response(status.HTTP_404_NOT_FOUND)
		if role(request) == "admin":
			user.groups.remove(group)
			return reverse("group", kwargs={"group_id": group_id})
		else:
			return Response(status.HTTP_401_UNAUTHORIZED)

class TestsView(View):
	form = TestsForm

	def get(self, request):
		tests = Test.objects.all()
		results = []
		for test in tests:
			if request.user.has_perm('do_test', test) or request.user == test.teacher:
				results.append({
					"id": test.id,
					"url": reverse("test", kwargs={"test_id": test.id}),
				})
		return results

	def post(self, request):
		if role(request) != "teacher":
			return Response(status.HTTP_401_UNAUTHORIZED)

		test = Test.objects.create(**{
			"teacher": request.user,
			"list": self.CONTENT["list"],
		})
		return reverse("test", kwargs={"test_id": test.id})

class TestView(View):
	def get(self, request, test_id):
		try:
			test = Test.objects.get(id=test_id)
		except ObjectDoesNotExist:
			return Response(status.HTTP_404_NOT_FOUND)
		result = {
			"id": test.id,
			"teacher": reverse("user", kwargs={"id": test.teacher.id}),
			"url": reverse("test", kwargs={"test_id": test_id}),
			"students": reverse("test_students", kwargs={"test_id": test_id}),
			"groups": reverse("test_groups", kwargs={"test_id": test_id}),
			"answers": reverse("test_answers", kwargs={"test_id": test_id}),
			"checked_answers": reverse("test_checked_answers", kwargs={"test_id": test_id}),
		}
		if request.user == test.teacher:
			result["list"] = test.list
			return result
		elif request.user.has_perm('do_test', test):
			result["list"] = self._strip_answers(test.list)
			return result
		else:
			return Response(status.HTTP_401_UNAUTHORIZED)

	def _strip_answers(self, list):
		list = json.loads(list)
		if "tests" in list:
			del list["tests"]
		if "items" in list:
			for item in list["items"]:
				if "answers" in item:
					del item["answers"]
		return json.dumps(list)

	def delete(self, request, test_id):
		try:
			test = Test.objects.get(id=test_id)
		except ObjectDoesNotExist:
			return Response(status.HTTP_404_NOT_FOUND)
		if request.user == test.teacher:
			test.delete()
			return reverse("tests")
		else:
			return Response(status.HTTP_401_UNAUTHORIZED)

class TestGroupsView(View):
	form = TestGroupsForm

	def get(self, request, test_id):
		try:
			test = Test.objects.get(id=test_id)
		except ObjectDoesNotExist:
			return Response(status.HTTP_404_NOT_FOUND)
		if not test.teacher == request.user:
			return Response(status.HTTP_401_UNAUTHORIZED)
		groups = get_groups_with_perms(test, attach_perms=True)
		groups = filter(lambda x: groups[x] == "do_test", groups)
		results = []
		for group in groups:
			results.append(reverse("test_group", kwargs={"test_id": test_id, "group_id": group.id}))
		return results

	def post(self, request, test_id):
		try:
			test = Test.objects.get(id=test_id)
		except ObjectDoesNotExist:
			return Response(status.HTTP_404_NOT_FOUND)
		if test.teacher == request.user:
			group = self.CONTENT["group_id"]
			assign('do_test', group, test)
			return reverse("test_group", kwargs={"test_id": test_id, "group_id": group.id})
		else:
			return Response(status.HTTP_401_UNAUTHORIZED)

class TestGroupView(View):
	def get(self, request, test_id, group_id):
		return {
			"url": reverse("test_group", kwargs={"test_id": test_id, "group_id": group_id}),
			"group_url": reverse("group", kwargs={"group_id": group_id}),
			"test_id": reverse("test", kwargs={"test_id": test_id}),
		}

	def delete(self, request, test_id, group_id):
		try:
			test = Test.objects.get(id=test_id)
		except ObjectDoesNotExist:
			return Response(status.HTTP_404_NOT_FOUND)
		if test.teacher == request.user:
			try:
				group = Group.objects.get(id=group_id)
			except ObjectDoesNotExist:
				return Response(status.HTTP_404_NOT_FOUND)
			remove_perm('do_test', group, test)
			return reverse("test_groups", kwargs={"test_id": test_id})
		else:
			return Response(status.HTTP_401_UNAUTHORIZED)

class TestStudentsView(View):
	form = TestStudentsForm

	def get(self, request, test_id):
		try:
			test = Test.objects.get(id=test_id)
		except ObjectDoesNotExist:
			return Response(status.HTTP_404_NOT_FOUND)
		if not test.teacher == request.user:
			return Response(status.HTTP_401_UNAUTHORIZED)
		students = get_users_with_perms(test, attach_perms=True, with_group_users=False)
		students = filter(lambda x: "do_test" in students[x], students)
		results = []
		for student in students:
			results.append(reverse("test_student", kwargs={"test_id": test_id, "student_id": student.id}))
		return results

	def post(self, request, test_id):
		try:
			test = Test.objects.get(id=test_id)
		except ObjectDoesNotExist:
			return Response(status.HTTP_404_NOT_FOUND)
		if test.teacher == request.user:
			student = self.CONTENT["student_id"]
			assign('do_test', student, test)
			return reverse("test_student", kwargs={"test_id": test_id, "student_id": student.id})
		else:
			return Response(status.HTTP_401_UNAUTHORIZED)

class TestStudentView(View):
	def get(self, request, test_id, student_id):
		return {
			"url": reverse("test_student", kwargs={"test_id": test_id, "student_id": student_id}),
			"test": reverse("test", kwargs={"test_id": test_id}),
			"student": reverse("user", kwargs={"id": student_id})
		}

	def delete(self, request, test_id, student_id):
		try:
			test = Test.objects.get(id=test_id)
		except ObjectDoesNotExist:
			return Response(status.HTTP_404_NOT_FOUND)
		if test.teacher == request.user:
			try:
				student = User.objects.get(id=student_id)
			except ObjectDoesNotExist:
				return Response(status.HTTP_404_NOT_FOUND)
			remove_perm('do_test', student, test)
			return reverse("test_students", kwargs={"test_id": test_id})
		else:
			return Response(status.HTTP_401_UNAUTHORIZED)

class TestAnswersView(View):
	form = TestAnswersForm

	def get(self, request, test_id):
		try:
			test = Test.objects.get(id=test_id)
		except ObjectDoesNotExist:
			return Response(status.HTTP_404_NOT_FOUND)
		answers = Answers.objects.filter(test=test)
		results = []
		for answer in answers:
			if test.teacher == request.user or request.user == answer.student:
				results.append(reverse("test_answer", kwargs={"test_id": test_id, "student_id": answer.student.id}))
		return results

	def post(self, request, test_id):
		try:
			test = Test.objects.get(id=test_id)
		except ObjectDoesNotExist:
			return Response(status.HTTP_404_NOT_FOUND)
		if request.user.has_perm('do_test', test):
			try:
				answer = Answers.objects.create(**{
					"test": test,
					"student": request.user,
					"list": self.CONTENT["list"],
				})
			except IntegrityError:
				return Response(status.HTTP_400_BAD_REQUEST, "You can only hand in answers once.")
			return reverse("test_answer", kwargs={"test_id": test_id, "student_id": answer.student.id})
		else:
			return Response(status.HTTP_401_UNAUTHORIZED)

class TestAnswerView(View):
	form = TestAnswersForm

	def get(self, request, test_id, student_id):
		try:
			answer = Answers.objects.get(student=student_id)
		except ObjectDoesNotExist:
			return Response(status.HTTP_404_NOT_FOUND)
		if request.user in (answer.student, answer.test.teacher):
			return {
				"url": reverse("test_answer", kwargs={"test_id": test_id, "student_id": student_id}),
				"student": reverse("user", kwargs={"id": answer.student.id}),
				"test": reverse("test", kwargs={"test_id": test_id}),
				"list": answer.list,
			}
		else:
			return Response(status.HTTP_401_UNAUTHORIZED)

class TestCheckedAnswersView(View):
	form = TestCheckedAnswersForm

	def get(self, request, test_id):
		try:
			test = Test.objects.get(id=test_id)
		except ObjectDoesNotExist:
			return Response(status.HTTP_404_NOT_FOUND)
		checkedAnswers = CheckedAnswers.objects.filter(answer__test=test)
		results = []
		for checkedAnswer in checkedAnswers:
			if test.teacher == request.user or checkedAnswer.answer.student == request.user:
				results.append(reverse("test_checked_answer", kwargs={"test_id": test_id, "answer_id": checkedAnswer.answer.student.id}))
		return results

	def post(self, request, test_id):
		try:
			test = Test.objects.get(id=test_id)
		except ObjectDoesNotExist:
			return Response(status.HTTP_404_NOT_FOUND)
		if request.user == test.teacher:
			if self.CONTENT["answer_id"].test != test:
				return Response(status.HTTP_400_BAD_REQUEST, "This answer isn't associated with the current test.")
			try:
				checkedAnswer = CheckedAnswers.objects.create(**{
					"answer": self.CONTENT["answer_id"],
					"list": self.CONTENT["list"],
					"note": self.CONTENT["note"],
				})
			except IntegrityError:
				return Response(status.HTTP_400_BAD_REQUEST, "These answers have already been checked.")
			else:
				return reverse("test_checked_answer", kwargs={"test_id": test_id, "answer_id": checkedAnswer.answer.student.id})
		else:
			return Response(status.HTTP_401_UNAUTHORIZED)

class TestCheckedAnswerView(View):
	form = TestCheckedAnswerForm

	def get(self, request, test_id, answer_id):
		try:
			checkedAnswer = CheckedAnswers.objects.get(answer__student=answer_id)
		except ObjectDoesNotExist:
			return Response(status.HTTP_404_NOT_FOUND)
		if request.user in (checkedAnswer.answer.student, checkedAnswer.answer.test.teacher):
			return {
				"list": checkedAnswer.list,
				"note": checkedAnswer.note,
				"answer": reverse("test_answer", kwargs={"test_id": test_id, "student_id": answer_id}),
				"url": reverse("test_checked_answer", kwargs={"test_id": test_id, "answer_id": answer_id}),
			}
		else:
			return Response(status.HTTP_401_UNAUTHORIZED)

	def put(self, request, test_id, answer_id):
		try:
			checkedAnswer = CheckedAnswers.objects.get(answer__student=answer_id)
		except ObjectDoesNotExist:
			return Response(status.HTTP_404_NOT_FOUND)
		if checkedAnswer.answer.test.teacher == request.user:
			checkedAnswer.list = self.CONTENT["list"]
			checkedAnswer.note = self.CONTENT["note"]
			checkedAnswer.save()
			return reverse("test_checked_answer", kwargs={"test_id": test_id, "answer_id": answer_id})
		else:
			return Response(status.HTTP_401_UNAUTHORIZED)

	def delete(self, request, test_id, answer_id):
		try:
			checkedAnswer = CheckedAnswers.objects.get(answer__student=answer_id)
		except ObjectDoesNotExist:
			return Response(status.HTTP_404_NOT_FOUND)
		if checkedAnswer.answer.test.teacher == request.user:
			checkedAnswer.delete()
			return reverse("test_checked_answers", kwargs={"test_id": test_id})
		else:
			return Response(status.HTTP_401_UNAUTHORIZED)
