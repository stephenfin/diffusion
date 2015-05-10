# Copyright 2015, Stephen Finucane <stephenfinucane@hotmail.com>
#
# This file is part of diffusion.

from __future__ import unicode_literals

from rest_framework import serializers

from diffusion.models import Person, Project, Issue, Series, Patch, Comment


class PersonSerializer(serializers.ModelSerializer):
    """
    Serialize a :model:`diffusion.Person`.
    """
    class Meta:
        model = Person
        fields = ('id', 'name', 'email')


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serialize a :model:`diffusion.Project`.
    """
    class Meta:
        model = Project
        fields = (
            'name', 'description', 'list_id', 'list_email', 'web_url',
            'scm_url', 'webscm_url')


class IssueSerializer(serializers.ModelSerializer):
    """
    Serialize a :model:`diffusion.Issue`.
    """
    author = PersonSerializer(read_only=True)

    class Meta:
        model = Issue
        exclude = ('project', )
        read_only_fields = ('number', 'created_at', 'closed_at', 'updated_at')


class SeriesSerializer(IssueSerializer):
    """
    Serialize a :model:`diffusion.Series`.
    """
    class Meta:
        model = Series
        exclude = ('project', )
        read_only_fields = ('number', 'state', 'created_at', 'closed_at',
                            'updated_at')


class PatchSerializer(IssueSerializer):
    """
    Serialize a :model:`diffusion.Patch`.
    """
    class Meta:
        model = Patch
        exclude = ('project', )
        read_only_fields = ('number', 'sha', 'created_at', 'closed_at',
                            'updated_at')


class CommentSerializer(serializers.ModelSerializer):
    """
    Serialize a :model:`diffusion.Comment`.
    """
    class Meta:
        model = Comment
        read_only_fields = ()
