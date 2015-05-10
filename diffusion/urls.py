# Copyright 2015, Stephen Finucane <stephenfinucane@hotmail.com>
#
# This file is part of diffusion.

# pylint: disable=invalid-name

from django.conf.urls import include, patterns, url
from django.contrib import admin

from rest_framework_nested import routers

from diffusion.views.api import (
    PersonViewSet, ProjectViewSet, IssueViewSet, SeriesViewSet, PatchViewSet,
    CommentViewSet)


router = routers.SimpleRouter()
router.register(r'people', PersonViewSet)
router.register(r'projects', ProjectViewSet)

project_router = routers.NestedSimpleRouter(
    router, r'projects', lookup='project')
project_router.register(r'issues', IssueViewSet)
project_router.register(r'series', SeriesViewSet)
project_router.register(r'patches', PatchViewSet)

issue_router = routers.NestedSimpleRouter(
    project_router, r'issues', lookup='issue')
issue_router.register(r'comments', CommentViewSet)

urlpatterns = patterns(
    'diffusion.views',
    #
    # Web UI
    #

    # Index
    url(r'^$', 'index.index', name='home'),

    # Projects
    url(r'^project/(?P<project_id>[^/]+)/list/$',
        'project.patches'),

    # Patches
    url(r'^patch/$', 'patch.patch', name='patch'),

    #
    # API
    #

    url(r'^api/', include(router.urls)),
    url(r'^api/', include(project_router.urls)),
    url(r'^api/', include(issue_router.urls)),

    #
    # Admin
    #

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
