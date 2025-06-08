from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.containers import Grid
from textual.widgets import Label, Button


class ConfirmationDialog(ModalScreen[str]):
    CSS = """
    ConfirmationDialog {
        align: center middle;
    }

    #dialog {
        grid-size: 2;
        grid-gutter: 1 2;
        grid-rows: 1fr 3;
        padding: 0 1;
        width: 60;
        height: 11;
        background: $surface;
    }
    
    #question {
        column-span: 2;
        height: 1fr;
        width: 1fr;
        content-align: center middle;
    }

    Button {
        width: 100%;
    }
    """


    def __init__(self, message: str, btn_yes: str, btn_no: str):
        self.message = message
        self.btn_yes = btn_yes
        self.btn_no = btn_no
        super().__init__()


    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self.message, id="question"),
            Button(self.btn_yes, variant="error", id="yes"),
            Button(self.btn_no, variant="primary", id="no"),
            id="dialog",
        )

    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id)
