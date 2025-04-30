# toolbar.py
"""Toolbar module for markdown_editor."""

import ipywidgets as widgets

class Toolbar:
    """Create formatting buttons for editor."""

    def __init__(self):
        """Initialize formatting toolbar."""
        self.buttons = []

    def add(self, label: str, handler):
        """Add a button to the toolbar.

        Args:
            label: Button text.
            handler: Function to call on click.
        """
        btn = widgets.Button(description=label)
        btn.on_click(lambda b: handler())
        self.buttons.append(btn)

    def widget(self) -> widgets.HBox:
        """Return the toolbar as a horizontal box."""
        return widgets.HBox(self.buttons)
