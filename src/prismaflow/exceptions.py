"""
title: Exceptions raised by prisma-flow.
"""


class PrismaFlowError(Exception):
    """
    title: Base exception for prisma-flow errors.
    """


class TemplateNotSupportedError(PrismaFlowError):
    """
    title: Raised when a requested PRISMA template is not implemented.
    """


class OptionalDependencyError(PrismaFlowError):
    """
    title: Raised when an optional runtime dependency is not installed.
    """


class PrismaValidationError(PrismaFlowError):
    """
    title: Raised when a flow has validation errors.
    """
