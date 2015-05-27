# Copyright 2015, Stephen Finucane <stephenfinucane@hotmail.com>
#
# This file is part of diffusion.

from __future__ import absolute_import, unicode_literals

from django.http import HttpResponse
from django.shortcuts import render

from diffusion.models import Issue, Patch, Project


def project(request, project_id):
    return HttpResponse('')


def issues(request, project_id):
    context = {
        'issues': Issue.objects.all(),
        'project': Project.objects.get(list_id=project_id),
    }

    return render(request, 'diffusion/project_issues.html', context)


def series(request, project_id):
    return HttpResponse('')


def patches(request, project_id):
    context = {
        'patches': Patch.objects.all(),
        'project': Project.objects.get(list_id=project_id),
    }

    return render(request, 'diffusion/project_patches.html', context)
