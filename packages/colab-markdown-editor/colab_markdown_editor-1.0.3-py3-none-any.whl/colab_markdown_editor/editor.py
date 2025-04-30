# editor.py
"""Editor module for markdown_editor."""

import ipywidgets as widgets

class MarkdownEditor:
    """Manage the markdown text editor.

    Attributes:
        area (widgets.Textarea): The text area widget.
    """

    def __init__(self, height: str = '400px'):
        """Initialize the text area widget."""
        self.area = widgets.Textarea(
            placeholder='Edit your Markdown here...',
            layout=widgets.Layout(width='100%', height=height)
        )

    def set_text(self, text: str):
        """Load text into the editor.

        Args:
            text: Markdown text to display.
        """
        self.area.value = text

    def get_text(self) -> str:
        """Return the current editor content.

        Returns:
            The markdown text.
        """
        return self.area.value

    def bind(self, callback):
        """Bind a callback on text change.

        Args:
            callback: Function to call when text changes.
        """
        self.area.observe(lambda change: callback(change['new']), names='value')
