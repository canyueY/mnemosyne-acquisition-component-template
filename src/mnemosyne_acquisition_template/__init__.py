"""Template only. Importing this package does not connect to any service."""

from .errors import TemplateNotImplementedError
from .stubs import TemplateMnemosyneBridge, TemplateResearchHook, TemplateSourceAdapter

__version__ = "0.1.0"
TEMPLATE_ONLY = True

__all__ = [
    "TEMPLATE_ONLY",
    "TemplateNotImplementedError",
    "TemplateMnemosyneBridge",
    "TemplateResearchHook",
    "TemplateSourceAdapter",
]
