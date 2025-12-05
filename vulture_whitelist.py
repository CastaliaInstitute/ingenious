"""Vulture whitelist file.

This file contains patterns that vulture should ignore.
These are false positives for pytest fixtures, mock/stub functions, etc.
"""

# Pytest fixtures - these are injected by pytest and the variable name is required
# vulture sees them as unused but they're required for the test to run
azure_sdk_compat = None  # pytest fixture for SDK compatibility
mock_ingenious_settings = None  # pytest fixture for mocked settings

# Variables that look unused but are captured/referenced via closures or mocking
query_texts = None  # Used as mock method parameter - signature matters for type checking

# Pydantic model post init - parameter required by signature but not used
_context = None  # Required by pydantic model_post_init signature

# Tool function parameters - required for API but implementation is demo/mock
_ticker = None  # Demo tool function parameter
_date = None  # Demo tool function parameter
_topic = None  # Tool function parameter for KB agent search
