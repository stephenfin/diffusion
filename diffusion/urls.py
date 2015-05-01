# Copyright 2015, Stephen Finucane <stephenfinucane@hotmail.com>
#
# This file is part of diffusion.

from django.conf.urls import include, patterns, url
from django.contrib import admin


# pylint: disable=invalid-name
urlpatterns = patterns(
    'diffusion.views',
    # Index
    url(r'^$', 'index.index', name='home'),

    # Projects
    url(r'^project/(?P<project_id>[^/]+)/list/$',
        'project.patches'),

    # Patches
    url(r'^patch/$', 'patch.patch', name='patch'),

    # Admin
    url(r'^admin/', include(admin.site.urls)),
)
