# Colab Markdown Editor

<div id="badges" align="center">
    <a href="https://pypi.org/project/colab_markdown_editor">
        <img src="https://img.shields.io/pypi/v/colab_markdown_editor.svg" alt="vnstock download badge"/>
    </a>
    <a href="https://pypi.org/project/colab_markdown_editor/">
        <img src="https://img.shields.io/pypi/dm/colab_markdown_editor?label=downloads&style=flat" alt="colab_markdown_editor download badge"/>
    </a>
    <a target="_blank" href="https://colab.research.google.com/github/thinh-vu/colab_markdown_editor/blob/main/dev/colab_markdown_editor.ipynb?hl=en">
      <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
    </a>
    <a href="https://codespaces.new/thinh-vu/colab_markdown_editor">
      <img src="https://github.com/codespaces/badge.svg" height="20" />
    </a>
</div>

> An **interactive Markdown editor** tailored exclusively for **Google Colab** notebooks. Edit, preview, and manage local `.md` files directly within Colab’s UI—no external apps required.

![colab_markdown_editor](https://github.com/thinh-vu/colab_markdown_editor/blob/main/assets/colab_markdown_editor.png?raw=true)

---

## 🚀 Features

- **File Browser**  
  • Browse and load any `.md` file from the Colab VM or a mounted Google Drive.  
  • Use the dropdown to pick from all discovered markdown files under a chosen folder.  
  • Or switch to path-input mode to type a full filename (e.g. `notes/meeting.md`)—if it doesn’t exist yet, it will be created when you load it.  
  • Mount your Google Drive with one click, then navigate straight into your Drive tree.
  
- **Formatting Toolbar**  
  Bold, italic, headings, lists, links, images, and code insertion via buttons or Ctrl-shortcuts.

- **Word Count & Reading Time**  
  Live update of total words and estimated minutes to read, shown above the History panel.

- **Manual Save (💾) & Auto-Save**  
  Click the Save button at any time, or rely on the built-in autosave every few seconds.

- **View Modes**  
  Split (editor + preview), Edit only, or Preview only.

- **History**  
  Toggle the log of all past edits for quick undo or review.


---

## 📦 Installation

```bash
pip install colab_markdown_editor
```

---

## 🎯 Usage in Google Colab

1. **Open a Colab notebook**.
2. In a code cell, run:

```python
%run -m colab_markdown_editor
```

