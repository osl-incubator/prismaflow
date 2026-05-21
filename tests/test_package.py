"""Package scaffold tests."""

import prisma_flow


def test_version_is_available() -> None:
    """The package exposes its release-managed version."""
    assert prisma_flow.__version__
