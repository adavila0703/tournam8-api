import app
from unittest.mock import Mock
import pytest

res = Mock()
req = Mock()

@pytest.mark.asyncio
async def test_home():
    response = await app.home(res, req)
    assert response == 'Welcome to the Tournam8 API!!!'