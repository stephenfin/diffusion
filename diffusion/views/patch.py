# Copyright 2015, Stephen Finucane <stephenfinucane@hotmail.com>
#
# This file is part of diffusion.

from __future__ import absolute_import, unicode_literals

from django.http import HttpResponse


def patch(request, project_id, patch_id=None):
    return HttpResponse('')


def diff(request, project_id, patch_id):
    return HttpResponse('')


def mbox(request, project_id, patch_id):
    return HttpResponse('')
