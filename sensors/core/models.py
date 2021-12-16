# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils import timezone


class CoreQuerySet(models.QuerySet):
    pass


class CoreModelManager(models.Manager):
    pass

class CoreModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True