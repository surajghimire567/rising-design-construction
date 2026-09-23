from .base import *  # noqa: F403
import os

# Handy local default, but a deliberate DEBUG=False in .env remains respected.
if "DEBUG" not in os.environ:
    DEBUG = True