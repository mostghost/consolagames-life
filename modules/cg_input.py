import platform

if platform.system() == "Windows":
    import msvcrt
else:
    import sys
    import termios
    import fcntl
    import os
    import select


class CGInput:
    def __init__(self):
        if platform.system() == "Windows":

            self._get_input = self._windows_input

        else:
            # Linux input handling is marginally more complex than windows.
            # This is apparently because windows, on the command prompt side, is handled
            # character by character, but linux handles entire sentences as it is
            # meant to be sent online to a server once the sentence is finished.
            # So to get a single character input is a lot more tricky.

            # This grabs the 'file descriptor'/index for the standard input, usually 0
            fd = sys.stdin.fileno()
            # We make a copy of the terminal settings, these will be modified.
            term_mod = termios.tcgetattr(fd)
            # We're modifying local terminal settings by disabling buffering and
            # terminal echo, to make sure input is directly accessible.
            term_mod[3] = term_mod[3] & ~termios.ICANON & ~termios.ECHO
            # Now that the settings are changed we're reapplying them.
            termios.tcsetattr(fd, termios.TCSANOW, term_mod)
            # We're grabbing all old status flags for file descriptor fd. These control
            # the behavior of the fd, including blocking/non-blocking mode.
            old_flags = fcntl.fcntl(fd, fcntl.F_GETFL)
            # We're reapplying all old flags but also adding in non-blocking mode. This
            # will not block execution if no key is pressed, it'll just return nothing.
            fcntl.fcntl(fd, fcntl.F_SETFL, old_flags | os.O_NONBLOCK)

            self._get_input = self._linux_input

    def update(self):
        inp = self._get_input()

        if inp in ["Q",   # Pause
                   "E",   # Toggle
                   "O",   # Quit
                   "W",   # Up
                   "A",   # Left
                   "S",   # Down
                   "D",   # Right
                   "B",   # Preset 1
                   "N",   # Preset 2
                   "M"]:  # Preset 3
            return inp

    def _windows_input(self):
        if msvcrt.kbhit():
            key = msvcrt.getch()

        char = key.decode("ASCII")
        if char.isalpha():
            return char.upper()
        else:
            return None

    def _linux_input(self):

        last_char = None
        # Here we'll start a loop, but we'll break out of it quickly. However we will
        # continue going through the loop if there are multiple keys held down.
        while True:
            # This will grab any keys that are ready to be read from the standard input,
            # while discarding writable or exceptional conditions since we don't care
            # about those. The '0' signifies that it will spend 0 seconds waiting on an
            # input. If there is no input, 'in_list' will be empty.
            in_list, _, _ = select.select([sys.stdin], [], [], 0)
            if in_list:
                c = sys.stdin.read(1)
                if c:
                    # Because we're in a loop, we'll keep overwriting this.
                    last_char = c
                else:
                    break
            else:
                break
        # There is a problem with this code. Because we waited for 0 seconds, any key
        # presses past the first one will be discarded. This will correctly get rid of
        # any buffer left over from previous key presses, but should we manage to press
        # two+ keys in the next buffer the game will only accept the first one, and not
        # the most recent key. At a high frame rate though, this is not an issue.

        if last_char:
            if last_char.isalpha():
                return last_char.upper()
