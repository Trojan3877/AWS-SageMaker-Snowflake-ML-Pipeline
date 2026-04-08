# tests/conftest.py
"""
Pytest configuration: mock heavy cloud/db dependencies so unit tests
can run without real Snowflake or AWS credentials.
"""

import sys
from unittest.mock import MagicMock

# Mock snowflake.connector before any src modules are imported
snowflake_mock = MagicMock()
sys.modules.setdefault('snowflake', snowflake_mock)
sys.modules.setdefault('snowflake.connector', snowflake_mock.connector)
