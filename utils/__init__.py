import asyncio
import inspect
from contextlib import suppress


def requires_arguments(definition):
    """Returns True if the function takes arguments, False otherwise.

    Args:
        definition: The function or class to check.

    Returns:
        True if the function takes arguments, False otherwise.
    """
    
    if inspect.isclass(definition):
        return definition.__init__.__code__.co_argcount > 1
    
    return definition.__code__.co_argcount > 0

async def kill_tasks():
    loop = asyncio.get_event_loop()
    pending = asyncio.all_tasks(loop)

    for task in pending:
        task.cancel()
        
        with suppress(asyncio.CancelledError):
            await task 

def init(definition):
    if not requires_arguments(definition):
        return definition()
    
    def wrapper(*args, **kwargs):
        return definition(*args, **kwargs)
    
    return wrapper