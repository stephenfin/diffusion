# Copyright 2015, Stephen Finucane <stephenfinucane@hotmail.com>
#
# This file is part of diffusion.

from __future__ import absolute_import, unicode_literals

from django.shortcuts import render


def patch(request, project_id, patch_id=None):
    context = None

    if project_id:
        pass

    if patch_id:
        pass

    return render(request, 'diffusion/patch.html', context)
