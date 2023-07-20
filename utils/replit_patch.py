from .background import keep_alive


def replit_patch(debug_mode):
    if not debug_mode:
        keep_alive(debug_mode)
