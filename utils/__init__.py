"""
copyright 2025 miuruwa
"""

import asyncio
from contextlib import suppress

async def kill_tasks():
    """
    end tasks to close scripts without warns
    """
    loop = asyncio.get_event_loop()
    pending = asyncio.all_tasks(loop)

    for task in pending:
        task.cancel()

        with suppress(asyncio.CancelledError):
            await task
