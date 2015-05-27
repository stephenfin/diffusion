# Copyright 2015, Stephen Finucane <stephenfinucane@hotmail.com>
#
# This file is part of diffusion.

from __future__ import absolute_import, unicode_literals

from django.shortcuts import render

from diffusion.models import Project


def index(request):
    context = {
        'projects': Project.objects.all(),
    }

    return render(request, 'diffusion/index.html', context)
