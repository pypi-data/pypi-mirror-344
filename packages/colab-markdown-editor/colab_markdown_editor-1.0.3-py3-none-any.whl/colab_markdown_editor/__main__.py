#!/usr/bin/env python3
"""Main launcher for markdown_editor in Google Colab."""

import os
import time
import ipywidgets as widgets
from ipywidgets import HBox, VBox, Layout
from IPython.display import display, HTML, clear_output
from .editor import MarkdownEditor
from .preview import PreviewPane
from .filemgr import FileManager
from .autosave import AutoSaver
from .history import HistoryLog


class App:
    """Glue all components and launch the editor in Colab."""

    def __init__(self):
        """Instantiate components, add CSS classes, and build UI."""
        # Core editor components
        self.editor  = MarkdownEditor()
        # Ensure JS toolbar can locate our <textarea>
        self.editor.area.add_class('editor-textarea')
        self.preview = PreviewPane()
        self.files   = FileManager()
        self.history = HistoryLog()
        self.saver   = AutoSaver(interval=5, save_fn=self._save)

        # File Browser toolbar
        self.local_btn     = widgets.Button(icon='desktop',     description='📁 Local')
        self.drive_btn     = widgets.Button(icon='hdd',         description='☁ Drive')
        self.path_btn      = widgets.Button(icon='folder-open', description='🗃 Path')
        self.file_dropdown = widgets.Dropdown(options=[],       description='')
        self.file_dropdown.layout.display = 'none'
        self.path_input    = widgets.Text(placeholder='Path or new file')
        self.path_input.layout.display = 'none'
        self.load_btn      = widgets.Button(icon='folder-open', description='📂 Load')
        self.save_lbl      = widgets.Label(value='Ready')

        # Formatting toolbar DIV
        toolbar_html = """
<div class="md-toolbar">
  <button onclick="applyMd('**bold**')" title="Bold (Ctrl+B)"><b>B</b></button>
  <button onclick="applyMd('*italic*')" title="Italic (Ctrl+I)"><i>I</i></button>
  <button onclick="applyMd('# Heading')" title="Heading (Ctrl+H)">H</button>
  <button onclick="applyMd('- item')" title="List (Ctrl+L)">•</button>
  <button onclick="applyMd('![alt](url)')" title="Image (Ctrl+G)">🖼️</button>
  <button onclick="applyMd('[text](url)')" title="Link (Ctrl+K)">🔗</button>
  <button onclick="applyMd('```\\ncode\\n```')" title="Code (Ctrl+`)">💻</button>
</div>
"""
        self.toolbar_div = widgets.HTML(
            value=toolbar_html,
            layout=Layout(width='100%'),
            sanitize=False  # keep onclick handlers
        )

        # Scripts & styles for toolbar (executed on load)
        script = """
<style>
.md-toolbar {
  background: var(--jp-layout-color2);
  color: var(--jp-ui-font-color1);
  padding:8px; border:1px solid var(--jp-border-color2);
  display:flex; gap:8px; align-items:center;
}
.md-toolbar button {
  background: var(--jp-layout-color1);
  color: var(--jp-ui-font-color1);
  border:none; padding:4px 8px; border-radius:4px;
  cursor:pointer;
}
.md-toolbar button:hover {
  background: var(--jp-layout-color3);
}
</style>
<script>
function applyMd(md) {
  const container = document.querySelector('.editor-textarea');
  if (!container) return;
  const ta = container.querySelector('textarea');
  if (!ta) return;
  const { selectionStart: s, selectionEnd: e, value: v } = ta;
  ta.value = v.slice(0, s) + md + v.slice(e);
  ta.focus();
  ta.selectionEnd = s + md.length;
  ta.dispatchEvent(new Event('input', { bubbles: true }));
}
document.addEventListener('keydown', e => {
  if (!e.ctrlKey) return;
  const map = { b:'**bold**', i:'*italic*', h:'# Heading',
                l:'- item', g:'![alt](url)', k:'[text](url)',
                '`':'```\\ncode\\n```' };
  const md = map[e.key];
  if (md) { e.preventDefault(); applyMd(md); }
});
</script>
"""
        self.script = HTML(script)

        # View mode dropdown
        self.mode_sel = widgets.Dropdown(
            options=[('🔲 Split','split'), ('✏️ Edit','edit'), ('👁️ View','view')],
            description='Mode:',
            layout=Layout(width='140px')
        )

        # History toggle
        self.hist_toggle = widgets.ToggleButton(icon='history', description='🕐 History')
        self.hist_box    = widgets.Output()

        # Word count and reading time stats
        self.stats_lbl = widgets.Label(value="Words: 0 | Reading time: 1 min")

        # Force Save button
        self.force_save_btn = widgets.Button(
            icon='save',
            description='💾 Save',
            button_style='success',
            tooltip='Force save the file'
        )
        self.force_save_btn.on_click(lambda _: self._force_save())

        # Main area container
        self.main_area = VBox()

        # Wire callbacks
        self._wire()

    def _wire(self):
        """Hook up widget events."""
        self.local_btn.on_click(lambda _: self._browse(os.getcwd()))
        self.drive_btn.on_click(
            lambda _: (self.files.mount_drive(), self._browse('/content/drive'))
        )
        self.path_btn.on_click(lambda _: self._show_path())
        self.file_dropdown.observe(lambda ch: self._load(ch['new']), names='value')
        self.load_btn.on_click(lambda _: self._load(self.path_input.value.strip()))
        self.editor.bind(self._on_edit)
        self.mode_sel.observe(self._switch_view, names='value')
        self.hist_toggle.observe(self._toggle_history, names='value')

    def _browse(self, root):
        """Populate dropdown with .md files under root."""
        files = self.files.search(root)
        self.file_dropdown.options = [(os.path.basename(f), f) for f in files]
        self.file_dropdown.layout.display = 'block'
        self.path_input.layout.display = 'none'

    def _show_path(self):
        """Show only path input."""
        self.file_dropdown.layout.display = 'none'
        self.path_input.layout.display = 'flex'

    def _load(self, path):
        """Load or create then display the file."""
        if not path:
            return
        if not path.endswith('.md'):
            path += '.md'
        if os.path.exists(path):
            content = self.files.load(path)
        else:
            content = ''
            self.files.save(path, content)
        self.editor.set_text(content)
        self.preview.render(content)
        self.save_lbl.value = f'Loaded {os.path.basename(path)}'
        self._update_stats(content)

    def _on_edit(self, text):
        """Handle editor changes."""
        self.preview.render(text)
        if self.files.path:
            self.files.save(self.files.path, text)
        self.save_lbl.value = time.strftime('%H:%M:%S')
        self.history.record(text)
        self._update_stats(text)

    def _save(self):
        """Autosave callback."""
        txt = self.editor.get_text()
        if self.files.path:
            self.files.save(self.files.path, txt)
            self.save_lbl.value = time.strftime('%H:%M:%S')

    def _force_save(self):
        """Force save the current file."""
        self._save()
        self.save_lbl.value = "File saved manually!"

    def _switch_view(self, change):
        """Rebuild main_area for split/edit/view."""
        mode = change['new']
        if mode == 'split':
            left  = VBox(
                [self.toolbar_div, self.editor.area],
                layout=Layout(width='50%')
            )
            right = VBox(
                [self.preview.widget()],
                layout=Layout(width='50%')
            )
            self.main_area.children = [HBox([left, right], layout=Layout(width='100%'))]
        elif mode == 'edit':
            self.main_area.children = [
                VBox([self.toolbar_div, self.editor.area], layout=Layout(width='100%'))
            ]
        else:  # view
            self.main_area.children = [
                VBox([self.preview.widget()], layout=Layout(width='100%'))
            ]

    def _toggle_history(self, change):
        """Show or hide history."""
        with self.hist_box:
            clear_output()
            if change['new']:
                display(self.history.widget())

    def _update_stats(self, content):
        """Update the words count and reading time."""
        words = len(content.split())
        reading_time = max(1, words // 200)  # Assuming 200 words/min reading speed
        self.stats_lbl.value = f"Words: {words} | Reading time: {reading_time} min"

    def launch(self):
        """Render the UI and start autosave."""
        # Inject toolbar scripts/styles
        display(self.script)

        # Top file browser row
        file_row = HBox([
            self.local_btn, self.drive_btn, self.path_btn,
            self.file_dropdown, self.path_input, self.load_btn, self.save_lbl
        ], layout=Layout(margin='6px 0'))

        # Mode selector and stats row
        ctrl_row = HBox(
            [self.mode_sel, self.stats_lbl, self.force_save_btn],
            layout=Layout(justify_content='space-between', width='100%', margin='6px 0')
        )

        # History row
        hist_row = VBox([self.hist_toggle, self.hist_box], layout=Layout(margin='6px 0'))

        # Initial browse + load first file
        self._browse(os.getcwd())
        if self.file_dropdown.options:
            self._load(self.file_dropdown.options[0][1])

        # Default view + build main_area
        self.mode_sel.value = 'split'
        self._switch_view({'new': 'split'})

        # Display everything
        display(file_row, ctrl_row, self.main_area, hist_row)

        # Start autosave
        self.saver.start()


def main():
    """Entry point for console script."""
    app = App()
    app.launch()

if __name__ == '__main__':
    main()