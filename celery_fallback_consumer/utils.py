# -*- coding: utf-8 -*-

from __future__ import absolute_import

from celery import apps

__all__ = ['register']

def register(app):
    from .bootsteps import FallbackConsumer

    app.steps['consumer'].add(FallbackConsumer)
