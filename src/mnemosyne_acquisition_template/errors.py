"""Explicit failure for every unimplemented capability."""


class TemplateNotImplementedError(NotImplementedError):
    """The developer must implement this port in a derived component."""
