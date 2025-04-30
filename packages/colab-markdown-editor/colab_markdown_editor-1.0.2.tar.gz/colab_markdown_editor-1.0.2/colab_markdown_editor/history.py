# history.py
"""History module for markdown_editor."""

import ipywidgets as widgets
from datetime import datetime

class HistoryLog:
    """Record editor snapshots for history view."""

    def __init__(self):
        """Initialize the history log."""
        self.entries = []

    def record(self, text: str):
        """Add a new snapshot of editor content."""
        ts = datetime.now().strftime('%H:%M:%S')
        self.entries.append((ts, text))

    def widget(self) -> widgets.VBox:
        """Return a widget showing recent snapshots."""
        items = []
        for ts, txt in self.entries[-10:]:
            snippet = txt.replace('\n', ' ')[:80] + '…'
            items.append(widgets.HTML(f'<b>{ts}</b>: {snippet}'))
        return widgets.VBox(items)
