import platform
import sys


class ConsoleInputHandler:
    """
    Handles non-blocking keyboard input for console mode.
    Platform-specific implementation for Windows and Unix-like systems.
    """

    def __init__(self):
        """Initialize the input handler."""
        self.system = platform.system()

        if self.system == "Windows":
            import msvcrt
            self.msvcrt = msvcrt
        else:
            import tty
            import termios
            self.tty = tty
            self.termios = termios
            self.old_settings = None

    def setup_terminal(self) -> None:
        """Setup terminal for raw input (Unix only)."""
        if self.system != "Windows" and sys.stdin.isatty():
            self.old_settings = self.termios.tcgetattr(sys.stdin)
            self.tty.setcbreak(sys.stdin.fileno())

    def restore_terminal(self) -> None:
        """Restore terminal to normal mode (Unix only)."""
        if self.system != "Windows" and self.old_settings is not None:
            self.termios.tcsetattr(
                sys.stdin, self.termios.TCSADRAIN, self.old_settings)

    def get_key(self) -> str | None:
        """
        Get a key press in a non-blocking way.
        Returns the key pressed or None if no key was pressed.
        """
        if self.system == "Windows":
            return self._get_key_windows()
        else:
            return self._get_key_unix()

    def _get_key_windows(self) -> str | None:
        """Get key press on Windows."""
        if self.msvcrt.kbhit():
            key = self.msvcrt.getch()

            # Handle special keys (arrows, function keys)
            if key in (b'\x00', b'\xe0'):
                # Extended key, read the next byte
                key = self.msvcrt.getch()
                # Arrow keys
                if key == b'H':  # Up arrow
                    return 'UP'
                elif key == b'P':  # Down arrow
                    return 'DOWN'
                elif key == b'K':  # Left arrow
                    return 'LEFT'
                elif key == b'M':  # Right arrow
                    return 'RIGHT'
            else:
                # Regular key
                try:
                    return key.decode('utf-8').lower()
                except:
                    return None
        return None

    def _get_key_unix(self) -> str | None:
        """Get key press on Unix-like systems."""
        import select

        # Check if there's input waiting
        dr, dw, de = select.select([sys.stdin], [], [], 0)
        if dr:
            ch = sys.stdin.read(1)

            # Handle escape sequences (arrow keys)
            if ch == '\x1b':  # ESC
                # Check if this is an escape sequence or just ESC
                dr, dw, de = select.select([sys.stdin], [], [], 0.01)
                if dr:
                    ch2 = sys.stdin.read(1)
                    if ch2 == '[':
                        ch3 = sys.stdin.read(1)
                        if ch3 == 'A':
                            return 'UP'
                        elif ch3 == 'B':
                            return 'DOWN'
                        elif ch3 == 'C':
                            return 'RIGHT'
                        elif ch3 == 'D':
                            return 'LEFT'
                else:
                    return 'ESCAPE'

            return ch.lower()

        return None
