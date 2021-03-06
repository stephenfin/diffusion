# Copyright 2015, Stephen Finucane <stephenfinucane@hotmail.com>
#
# This file is part of diffusion.

from __future__ import absolute_import, unicode_literals

from django.http import HttpResponse
from django.shortcuts import render


def project(request, project_id):
    return HttpResponse('')


def issues(request, project_id):
    return HttpResponse('')


def series(request, project_id):
    return HttpResponse('')


def patches(request, project_id):
    from datetime import datetime
    context = {
        'patches': [{
            'id': 1,
            'name': 'Add some tests',
            'date': datetime.now(),
            'submitter': {
                'name': 'John Doe',
                'email': 'john.doe@example.com',
            },
            'delegate': None,
            'state': 'New',
            'comment_count': 5,
        }],
    }

    if project_id:
        pass

    return render(request, 'diffusion/project_patches.html', context)
