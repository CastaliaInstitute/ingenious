"""Prompt templates package namespace extension.

This module extends the package namespace to include all subdirectories
on sys.path, effectively combining multiple modules into a single namespace.
This pattern is used for plugin-style architecture.
"""

from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
