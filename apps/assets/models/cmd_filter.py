# -*- coding: utf-8 -*-
#
import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _

from orgs.mixins import OrgModelMixin


__all__ = [
    'CommandFilter', 'CommandFilterRule'
]


class CommandFilter(OrgModelMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=64, verbose_name=_("Name"))
    is_active = models.BooleanField(default=True, verbose_name=_('Is active'))
    comment = models.TextField(blank=True, default='', verbose_name=_("Comment"))
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=128, blank=True, default='', verbose_name=_('Created by'))

    def __str__(self):
        return self.name


class CommandFilterRule(OrgModelMixin):
    TYPE_REGEX = 'regex'
    TYPE_COMMAND = 'command'
    TYPE_CHOICES = (
        (TYPE_REGEX, _('Regex')),
        (TYPE_COMMAND, _('Command')),
    )

    ACTION_DENY = 'deny'
    ACTION_ACCEPT = 'accept'
    ACTION_CHOICES = (
        (ACTION_DENY, _('Deny')),
        (ACTION_ACCEPT, _('Accept'))
    )

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    filter = models.ForeignKey('CommandFilter', on_delete=models.CASCADE, verbose_name=_("Filter"), related_name='rules')
    type = models.CharField(max_length=16, default=TYPE_COMMAND, choices=TYPE_CHOICES, verbose_name=_("Type"))
    priority = models.IntegerField(default=50, verbose_name=_("Priority"), validators=[MinValueValidator(1), MaxValueValidator(100)])
    content = models.TextField(max_length=1024, verbose_name=_("Content"), help_text=_("One line one command"))
    action = models.CharField(max_length=16, default=ACTION_DENY, choices=ACTION_CHOICES, verbose_name=_("Action"))
    comment = models.CharField(max_length=64, blank=True, default='', verbose_name=_("Comment"))
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=128, blank=True, default='', verbose_name=_('Created by'))

    def __str__(self):
        return '{} % {}'.format(self.type, self.content)
