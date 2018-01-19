from .base import *


INSTALLED_APPS += (
    'wagtail_personalisation',
    'wagtailfontawesome',
)

CELERY_ALWAYS_EAGER = True
BROKER_BACKEND = 'memory'

PERSONALISATION_SEGMENTS_ADAPTER = (
    'molo.surveys.adapters.PersistentSurveysSegmentsAdapter'
)
