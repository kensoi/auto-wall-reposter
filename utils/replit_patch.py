import sys

from .background import keep_alive


def replit_patch(debug_mode):
    if not debug_mode:
        if "vkbotkit" not in sys.modules:
            import pip
            pip.main(["install", "-r", "requirements.txt"])
        
        keep_alive(debug_mode)