# Copyright 2015, Stephen Finucane <stephenfinucane@hotmail.com>
#
# This file is part of diffusion.

from __future__ import unicode_literals

from django.contrib import admin

from diffusion.models import Person, Project, Issue, Series, Patch, Comment


class PersonAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')


class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')


class IssueAdmin(admin.ModelAdmin):
    readonly_fields = ('number', 'created_at', 'closed_at', 'updated_at')


class SeriesAdmin(admin.ModelAdmin):
    readonly_fields = ('number', 'state', 'created_at', 'closed_at',
                       'updated_at')


class PatchAdmin(admin.ModelAdmin):
    readonly_fields = ('number', 'sha', 'created_at', 'closed_at',
                       'updated_at')


class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', )


admin.site.register(Person, PersonAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Patch, PatchAdmin)
admin.site.register(Comment, CommentAdmin)
