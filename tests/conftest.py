import asyncio
import sys
import pytest

@pytest.fixture(scope="session", autouse=True)
def event_loop_policy():
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())