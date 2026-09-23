from os import environ
from .base import *  # noqa: F403

# Handy local default, but a deliberate DEBUG=False in .env remains respected.
if "DEBUG" not in environ:
    DEBUG = True
