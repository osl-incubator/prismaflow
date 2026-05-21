"""
title: Lightweight PRISMA-style flow diagram generation.
"""

from prismaflow.enums import PrismaTemplate
from prismaflow.exceptions import (
    OptionalDependencyError,
    PrismaFlowError,
    PrismaValidationError,
    TemplateNotSupportedError,
)
from prismaflow.models import (
    EligibilityStage,
    FlowMetadata,
    IdentificationStage,
    IncludedStage,
    PrismaFlow,
    ScreeningStage,
)
from prismaflow.validation import ValidationMessage, ValidationReport, validate_flow

__version__ = "0.1.0"

__all__ = [
    "EligibilityStage",
    "FlowMetadata",
    "IdentificationStage",
    "IncludedStage",
    "OptionalDependencyError",
    "PrismaFlow",
    "PrismaFlowError",
    "PrismaTemplate",
    "PrismaValidationError",
    "ScreeningStage",
    "TemplateNotSupportedError",
    "ValidationMessage",
    "ValidationReport",
    "__version__",
    "validate_flow",
]
