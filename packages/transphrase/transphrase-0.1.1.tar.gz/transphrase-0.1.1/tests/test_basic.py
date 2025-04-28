"""Basic tests for TransPhrase package."""

import pytest


def test_import():
    """Test that the package can be imported."""
    import transphrase

    assert hasattr(transphrase, "__version__")


def test_config_import():
    """Test that the config module can be imported."""
    from transphrase.core.config import DEFAULT_MODEL

    assert isinstance(DEFAULT_MODEL, str)
