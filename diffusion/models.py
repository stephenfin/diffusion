# Copyright 2015, Stephen Finucane <stephenfinucane@hotmail.com>
#
# This file is part of diffusion.

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import (
    Model, CharField, DateTimeField, TextField, ForeignKey, EmailField,
    PositiveIntegerField)
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
import datetime
import hashlib


class _Base(Model):
    """
    Share some common attributes and operations.
    """
    # timestamps

    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Person(_Base):
    """
    A :model:`diffusion.Person` represents a contributor to the mailing
    list.
    """
    # timestamps

    updated_at = DateTimeField(default=datetime.datetime.now)

    # content

    name = CharField(null=True, blank=True, max_length=255)
    email = EmailField(unique=True)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        super(Person, self).save(*args, **kwargs)

    def __str__(self):
        if self.name:
            return '%s <%s>' % (self.name, self.email)

    class Meta:
        verbose_name_plural = 'People'


@python_2_unicode_compatible
class Project(_Base):
    """
    A :model:`diffusion.Project` typically represents a specific
    mailing list.
    """
    # timestamps

    updated_at = DateTimeField(default=datetime.datetime.now)

    # content

    name = CharField(max_length=255, primary_key=True)
    description = TextField()
    list_id = CharField(max_length=255, unique=True,
        help_text='List-ID header, as described in RFC2919')
    list_email = EmailField(unique=True,
        help_text='List email address')

    # url metadate

    web_url = CharField(max_length=2000, blank=True)
    scm_url = CharField(max_length=2000, blank=True)
    webscm_url = CharField(max_length=2000, blank=True)

    def get_absolute_url(self):
        return reverse('diffusion.views.project.project', args=[self.name])

    def __str__(self):
        return 'Project <%s>' % (self.name, )


class _Email(_Base):
    """
    Base model for an email.
    """
    # parent

    project = ForeignKey(Project)

    # email metadata

    msgid = CharField(max_length=255)
    date = DateTimeField(default=datetime.datetime.now)
    headers = TextField(null=True, blank=True)

    # content

    author = ForeignKey(Person)
    title = CharField(null=True, blank=True, max_length=255)
    body = TextField(null=True, blank=True)

    class Meta:
        # unique_together = [('msgid', 'title')]
        abstract = True


@python_2_unicode_compatible
class Issue(_Email):
    """
    An :model:`diffusion.Issue` is a "root email" (i.e. the first
    email in a thread) or a patch. They should be specified as more
    specific classes, i.e. an :model:`diffusion.Series` or a
    :model:`diffusion.Patch` where applicable.
    """
    STATE_OPEN = 'open'
    STATE_CLOSED = 'closed'
    STATE_CHOICES = [
        (STATE_OPEN, 'Open'),
        (STATE_CLOSED, 'Closed')
    ]

    # timestamps

    updated_at = DateTimeField(default=datetime.datetime.now)
    closed_at = DateTimeField(null=True, blank=True)

    # context data

    number = PositiveIntegerField()
    state = CharField(choices=STATE_CHOICES, default=STATE_OPEN, max_length=10)

    def save(self, *args, **kwargs):
        self.number = self.project.issue_set.count() + 1
        super(Issue, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('diffusion.views.issue.issue', args=[
            self.project.name, self.number])

    def __str__(self):
        # TODO(sfinucan) - this is a bit of hack. It would be better if
        #   we could autodetect subclassing/proxying
        if hasattr(self, 'patch'):
            return 'Patch <%s>' % (self.msgid, )
        if hasattr(self, 'series'):
            return 'Series <%s>' % (self.msgid, )
        else:
            return 'Issue <%s>' % (self.msgid, )


class Series(Issue):
    """
    A :model:`diffusion.Series` is a specific type of issue - namely
    one that preceeds (in a threaded context) one or more patches. This
    typically takes the form of a cover letter, but can also be an
    empty email (in the case of a series of patches without said cover
    letter).
    """
    def __init__(self, *args, **kwargs):
        super(Series, self).__init__(*args, **kwargs)
        self.is_series = True

    # context data

    @property
    def has_patches(self):
        return getattr(self, 'patches').count() > 0

    def get_absolute_url(self):
        return reverse('diffusion.views.series.series', args=[
            self.project.name, self.number])

    class Meta:
        verbose_name_plural = 'Series'


class Patch(Issue):
    """
    A :model:`diffusion.Patch` is an even-more specific type of issue -
    namely one containing a diff. A oatch should never be the root
    element: it should, instead, refer to a :model:`diffusion.Series`
    as its "parent".
    """
    # parent

    series = ForeignKey(Series, related_name='patches')

    # context data

    sha = CharField(max_length=255)

    # content

    diff = TextField()
    version = CharField(max_length=16)

    # operations

    def save(self, *args, **kwargs):
        if self.diff:
            self.sha = hashlib.sha1(
                unicode(self.diff).encode('utf-8')).hexdigest()
        super(Patch, self).save(*args, **kwargs)

    def reopen(self):
        """Mark patch as 'open'.

        Patches are in the 'open' state by default, therefore it is only
        possible to reopen them.
        """
        self.state = Issue.STATE_OPEN
        self.closed_at = None
        self.save()

    def close(self):
        """Mark patch as 'closed'."""
        self.state = Issue.STATE_CLOSED
        self.closed_at = datetime.datetime.now()
        self.save()

    def get_absolute_url(self):
        return reverse('diffusion.views.patch.patch', args=[
            self.project.name, self.number])

    class Meta:
        verbose_name_plural = 'Patches'


@receiver(models.signals.post_save, sender=Patch)
def _patch_saved_callback(sender, created, instance, **kwargs):
    """Change state of a patch's series.

    Ensure that :model:`Series` state corresponds to the state of its
    child :model:`Patch` instances.
    """
    state = Issue.STATE_CLOSED

    series = instance.series
    for patch in series.patches.all():
        if patch.state == Issue.STATE_OPEN:
            state = Issue.STATE_OPEN
            break

    series.state = state
    series.save()


@python_2_unicode_compatible
class Comment(_Email):
    """
    A :model:`diffusion.Comment` is just that: a reply to an
    :model:`diffusion.Issue` (or any subclass thereof).
    """
    # parent

    issue = ForeignKey(Issue)

    def __str__(self):
        return 'Comment <%s>' % (self.msgid, )
