#!/usr/bin/env python3

import os
from unittest.mock import patch

# Clear environment to simulate the test
with patch.dict(os.environ, {}, clear=True):
    try:
        from ingenious.config.settings import IngeniousSettings

        settings = IngeniousSettings()
        print("Settings created successfully!")
        print(f"Number of models: {len(settings.models)}")
        if settings.models:
            print(f"First model: {settings.models[0]}")
    except Exception as e:
        print(f"Exception raised: {type(e).__name__}: {e}")
