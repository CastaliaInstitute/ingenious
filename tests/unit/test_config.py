import os
from unittest.mock import patch

import pytest
from ingenious.utils.env_substitution import substitute_env_vars


@pytest.mark.unit
class TestConfig:
    """Test Config class functionality"""

    def test_config_double_substitution(self):
        """Test that environment variables are substituted correctly when called multiple times"""
        yaml_content = "value: ${TEST_VAR:default}"

        with patch.dict(os.environ, {"TEST_VAR": "substituted"}, clear=True):
            # First substitution
            result1 = substitute_env_vars(yaml_content)
            # Second substitution (should not change the result)
            result2 = substitute_env_vars(result1)

            assert result1 == "value: substituted"
            assert result2 == "value: substituted"
