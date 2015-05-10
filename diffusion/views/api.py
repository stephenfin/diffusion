# Copyright 2015, Stephen Finucane <stephenfinucane@hotmail.com>
#
# This file is part of diffusion.

from __future__ import unicode_literals

from rest_framework import viewsets

from diffusion.models import Person, Project, Issue, Series, Patch, Comment
from diffusion.serializers import (
    PersonSerializer, ProjectSerializer, IssueSerializer, SeriesSerializer,
    PatchSerializer, CommentSerializer)


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer


class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer


class PatchViewSet(viewsets.ModelViewSet):
    queryset = Patch.objects.all()
    serializer_class = PatchSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
