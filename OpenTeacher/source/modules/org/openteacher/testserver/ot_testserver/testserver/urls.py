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

from django.conf.urls.defaults import patterns, include, url
from views import (
	IndexView,
	UsersView,
	UserView,
	UserMeView,
	GroupsView,
	GroupView,
	GroupMemberView,
	TestsView,
	TestView,
	TestGroupsView,
	TestGroupView,
	TestStudentsView,
	TestStudentView,
	TestAnswersView,
	TestAnswerView,
	TestCheckedAnswersView,
	TestCheckedAnswerView,
)

urlpatterns = patterns('',
	url(r'^/?$', IndexView.as_view(), name='index'),

	url(r'^users/?$', UsersView.as_view(), name='users'),
	url(r'^users/(?P<id>-?[0-9]+)/?$', UserView.as_view(), name='user'),
	url(r'^users/me/?$', UserMeView.as_view(), name='user_me'),

	url(r'^groups/?$', GroupsView.as_view(), name='groups'),
	url(r'^groups/(?P<group_id>-?[0-9]+)/?$', GroupView.as_view(), name='group'),
	url(r'^groups/(?P<group_id>-?[0-9]+)/(?P<student_id>-?[0-9]+)/?$', GroupMemberView.as_view(), name='group_member'),

	url(r'^tests/?$', TestsView.as_view(), name='tests'),
	url(r'^tests/(?P<test_id>-?[0-9]+)/?$', TestView.as_view(), name='test'),

	url(r'^tests/(?P<test_id>-?[0-9]+)/groups/?$', TestGroupsView.as_view(), name='test_groups'),
	url(r'^tests/(?P<test_id>-?[0-9]+)/groups/(?P<group_id>-?[0-9]+)/?$', TestGroupView.as_view(), name='test_group'),

	url(r'^tests/(?P<test_id>-?[0-9]+)/students/?$', TestStudentsView.as_view(), name='test_students'),
	url(r'^tests/(?P<test_id>-?[0-9]+)/students/(?P<student_id>-?[0-9]+)/?$', TestStudentView.as_view(), name='test_student'),

	url(r'^tests/(?P<test_id>-?[0-9]+)/answers/?$', TestAnswersView.as_view(), name='test_answers'),
	url(r'^tests/(?P<test_id>-?[0-9]+)/answers/(?P<student_id>-?[0-9]+)/?$', TestAnswerView.as_view(), name='test_answer'),

	url(r'^tests/(?P<test_id>-?[0-9]+)/checked_answers/?$', TestCheckedAnswersView.as_view(), name='test_checked_answers'),
	url(r'^tests/(?P<test_id>-?[0-9]+)/checked_answers/(?P<answer_id>-?[0-9]+)/?$', TestCheckedAnswerView.as_view(), name='test_checked_answer')
)
