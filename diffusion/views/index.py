# Copyright 2015, Stephen Finucane <stephenfinucane@hotmail.com>
#
# This file is part of diffusion.

from __future__ import absolute_import, unicode_literals

from django.shortcuts import render


def index(request):
    context = {
        'projects': [{
            'linkname': 'dpdk-dev',
            'name': 'Data Plane Development Kit Development Mailing List',
            'listemail': 'dev@dpdk.org',
            'web_url': 'http://www.dpdk.org/',
        }, {
            'linkname': 'openvswitch',
            'name': 'Open vSwitch Development Mailing List',
            'listemail': 'dev@openvswitch.org',
            'web_url': 'http://www.openvswitch.org/',
        }],
    }

    return render(request, 'diffusion/index.html', context)
