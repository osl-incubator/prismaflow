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
    new_review,
)
from prismaflow.validation import ValidationMessage, ValidationReport, validate_flow

__version__ = "0.4.0"  # semantic-release

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
    "new_review",
    "validate_flow",
]
