# preview.py
"""Preview module for markdown_editor."""

import ipywidgets as widgets
from IPython.display import Markdown, display, clear_output

class PreviewPane:
    """Render markdown in an Output widget."""

    def __init__(self, height: str = '400px'):
        """Initialize the preview pane widget."""
        self.out = widgets.Output(
            layout=widgets.Layout(width='100%', height=height, border='1px solid gray')
        )

    def render(self, text: str):
        """Render the given markdown text.

        Args:
            text: Markdown content to render.
        """
        with self.out:
            clear_output(wait=True)
            display(Markdown(text))

    def widget(self) -> widgets.Output:
        """Return the preview widget for display."""
        return self.out
