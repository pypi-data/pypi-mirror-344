from typing import Iterable

from textual import events, work, on
from textual.app import ComposeResult, App
from textual.binding import Binding
from textual.containers import Horizontal
from textual.events import Action
from textual.screen import ModalScreen
from textual.widget import Widget, AwaitMount
from textual.widgets import Input, Button


# noinspection PyUnresolvedReferences
class InputPopup(ModalScreen[str]):
    BINDINGS = [
        Binding("escape", "escape", show=False),
    ]

    DEFAULT_CSS = """
    InputPopup {
        align: center middle;
    }
    Dialog {
        border: solid $accent;
        width: 60%;
        height: 11;
        padding: 1 2;
        background: $panel;
    }
    Button {
        margin: 1 2;
    }
    Horizontal {
        align: center middle;
    }
    """

    class Dialog(Widget):

        def __init__(self, title: str, **kwargs):
            super().__init__(**kwargs)
            self.border_title = title

        def compose(self) -> ComposeResult:
            yield self.parent.input__
            yield Horizontal(
                Button("Ok", variant='success', id="ok"),
                Button("Cancel", variant='error', id="cancel"),
            )


    def __init__(self, title: str, current_value: str = '', **kwargs) -> None:
        super().__init__(**kwargs)
        self.title__ = title
        self.current_value__ = current_value
        self.input__ = Input(value=self.current_value__)
        self.value = current_value

    def compose(self) -> ComposeResult:
        yield self.Dialog(self.title__)

    @on(Button.Pressed, "#ok")
    def handle_ok(self) -> None:
        self.dismiss(self.input__.value)

    @on(Button.Pressed, "#cancel")
    def handle_cancel(self) -> None:
        self.dismiss(self.current_value__)

    @on(Input.Submitted)
    def handle_submit(self) -> None:
        self.dismiss(self.input__.value)

    def action_escape(self) -> None:
        self.dismiss(self.current_value__)


    async def show(self) -> str:
        return await self.app.push_screen_wait(self)


class TestApp(App):

    @work
    async def on_mount(self):
        i = await InputPopup('a value').show()
        self.notify(i)

if __name__ == '__main__':
    app = TestApp()
    app.run()

