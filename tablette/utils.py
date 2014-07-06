"""
    tablette.utils
    ~~~~~~~~~~~~~~

"""

__all__ = ['terminal_size']

import fcntl, termios, struct


def terminal_size():
    """Returns width and height of the console.
    """
    height, width, hp, wp = struct.unpack('HHHH',
        fcntl.ioctl(0, termios.TIOCGWINSZ,
        struct.pack('HHHH', 0, 0, 0, 0)))
    return width, height
