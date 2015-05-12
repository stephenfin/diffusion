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
router.register(r'people', PersonViewSet, 'people')
router.register(r'projects', ProjectViewSet, 'projects')

project_router = routers.NestedSimpleRouter(
    router, r'projects', lookup='project')
project_router.register(r'issues', IssueViewSet, 'issues')
project_router.register(r'series', SeriesViewSet, 'series')
project_router.register(r'patches', PatchViewSet, 'patches')

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
    url(r'^(?P<project_id>[^/]+)/$', 'project.project'),
    url(r'^(?P<project_id>[^/]+)/issues/$', 'project.issues'),
    url(r'^(?P<project_id>[^/]+)/series/$', 'project.series'),
    url(r'^(?P<project_id>[^/]+)/patches/$', 'project.patches'),

    # Issues

    url(r'^(?P<project_id>[^/]+)/issues/(?P<issue_id>\d+)$', 'issue.issue'),

    # Series

    url(r'^(?P<project_id>[^/]+)/issues/(?P<series_id>\d+)$', 'series.series'),

    # Patches

    url(r'^(?P<project_id>[^/]+)/patches/(?P<patch_id>\d+)$',
        'patch.patch'),
    url(r'^(?P<project_id>[^/]+)/patches/(?P<patch_id>\d+).diff$',
        'patch.diff'),
    url(r'^(?P<project_id>[^/]+)/patches/(?P<patch_id>\d+).mbox$',
        'patch.mbox'),

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
