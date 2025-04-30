# filemgr.py
"""File manager for markdown_editor."""

import os
import fnmatch
from google.colab import drive as _drive

class FileManager:
    """Handle markdown file operations."""

    def __init__(self):
        """Initialize file manager state."""
        self.path = None

    def search(self, root: str) -> list:
        """Find all .md files under a directory.

        Args:
            root: Directory to search.
        Returns:
            List of file paths.
        """
        matches = []
        for base, _, files in os.walk(root):
            for name in fnmatch.filter(files, '*.md'):
                matches.append(os.path.join(base, name))
        return matches

    def load(self, path: str) -> str:
        """Load markdown content from a file.

        Args:
            path: File path to load.
        Returns:
            File contents as a string.
        """
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.path = path
        return content

    def save(self, path: str, content: str):
        """Save markdown content to a file.

        Args:
            path: File path to write.
            content: Markdown text to save.
        """
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        self.path = path

    def mount_drive(self):
        """Mount Google Drive in Colab if not already mounted."""
        if not os.path.exists('/content/drive'):
            _drive.mount('/content/drive')
