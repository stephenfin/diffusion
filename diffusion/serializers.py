# Copyright 2015, Stephen Finucane <stephenfinucane@hotmail.com>
#
# This file is part of diffusion.

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
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
    html_url = serializers.URLField(source='get_absolute_url')
    issues_url = serializers.SerializerMethodField()
    series_url = serializers.SerializerMethodField()
    patches_url = serializers.SerializerMethodField()

    def get_issues_url(self, obj):
        return reverse('issues-list', kwargs={'project_pk': obj.name})

    def get_series_url(self, obj):
        return reverse('series-list', kwargs={'project_pk': obj.name})

    def get_patches_url(self, obj):
        return reverse('patches-list', kwargs={'project_pk': obj.name})

    class Meta:
        model = Project
        fields = ('name', 'html_url', 'list_id', 'list_email', 'description',
                  'web_url', 'scm_url', 'webscm_url', 'issues_url',
                  'series_url', 'patches_url')
        read_only_fields = ('html_url')


class IssueSerializer(serializers.ModelSerializer):
    """
    Serialize a :model:`diffusion.Issue`.
    """
    author = PersonSerializer(read_only=True)
    html_url = serializers.ReadOnlyField(source='get_absolute_url')

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
