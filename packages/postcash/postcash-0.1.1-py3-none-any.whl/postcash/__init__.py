# postcash/__init__.py

"""Asynchronous Notifications made easy with."""

__version__ = "0.1.1"

from .smtp import send_email

__all__ = ["send_email"]