# autosave.py
"""Autosave module for markdown_editor."""

import time
import threading

class AutoSaver:
    """Periodically save editor content."""

    def __init__(self, interval: int, save_fn):
        """Initialize the autosaver.

        Args:
            interval: Seconds between saves.
            save_fn: Callable to invoke to save content.
        """
        self.interval = interval
        self.save_fn = save_fn
        self._timer = None

    def _tick(self):
        """Invoke save and re-schedule the next tick."""
        try:
            self.save_fn()
        except Exception as e:
            print(f"Autosave error: {e}")
        finally:
            # schedule next save
            self._timer = threading.Timer(self.interval, self._tick)
            self._timer.daemon = True
            self._timer.start()

    def start(self):
        """Start the autosave loop."""
        if self._timer is None:
            self._timer = threading.Timer(self.interval, self._tick)
            self._timer.daemon = True
            self._timer.start()
