from __future__ import annotations

from typing import Any, ClassVar

from rich.syntax import Syntax
from textual import on
from textual.app import App, ComposeResult
from textual.binding import BindingType
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import DirectoryTree, Footer, Header, TextArea


class Sidebar(Container):
    def compose(self) -> ComposeResult:
        yield DirectoryTree("./")


class TextEditor(App):
    CSS_PATH = "assets/css/styles.tcss"
    BINDINGS: ClassVar[list[BindingType]] = [
        ("q", "quit", "Quit"),
        ("ctrl+s", "toggle_sidebar"),
    ]

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield Sidebar(classes="sidebar")
            with VerticalScroll():
                yield TextArea().code_editor(id="current-editor")
        yield Footer()

    def action_toggle_sidebar(self) -> None:
        self.query_one(Sidebar).toggle_class("-hidden")

    @on(TextArea.Changed, selector="current-editor")
    def handle_text_area_changed(self, event: TextArea.Changed):
        self.log(event)

    @on(DirectoryTree.FileSelected)
    def handle_file_selected(
        self, message: DirectoryTree.FileSelected
    ) -> None:

        self.sub_title = str(message.path)
        try:
            file_content = message.path.read_text()
        except UnicodeDecodeError:
            file_content = ""
            return None
        lexer = Syntax.guess_lexer(path=message.path.name, code=file_content)

        editor = self.query_one("#current-editor")
        editor.clear()
        try:
            editor.language = lexer
        except Exception:
            pass
        editor.text = file_content


app = TextEditor()
