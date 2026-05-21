"""
title: Enumerations used by prisma-flow.
"""

from enum import Enum


class PrismaTemplate(str, Enum):
    """
    title: Supported and planned PRISMA diagram templates.
    """

    PRISMA_2020_NEW_DATABASES_REGISTERS = "prisma_2020_new_databases_registers"
    PRISMA_2020_NEW_DATABASES_REGISTERS_OTHER = (
        "prisma_2020_new_databases_registers_other"
    )
    PRISMA_2020_UPDATED_DATABASES_REGISTERS = "prisma_2020_updated_databases_registers"
    PRISMA_2020_UPDATED_DATABASES_REGISTERS_OTHER = (
        "prisma_2020_updated_databases_registers_other"
    )
