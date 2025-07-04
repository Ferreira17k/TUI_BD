from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.containers import Grid
from textual.widgets import Label, Button, Input
from datetime import datetime
from input_field import input_field


class UpdateModal(ModalScreen[str]):
    CSS = """
    UpdateModal {
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
    
    #field {
        grid-size: 3;
        grid-columns: auto 1fr 7;
        column-span: 2;
        align: center middle;
        width: 100%;
    }

    Input {
        width: 100%;
    }

    Input.empty {
      color: tomato;
    }

    #confirm, #cancel {
        width: 100%;
    }

    #clear {
        width: 7;
        min-width: 0;
    }
    """


    def __init__(self, column, old_value):
        self.field_name, self.field_type, self.field_optional = column
        self.value = old_value
        super().__init__()


    def compose(self) -> ComposeResult:
        yield Grid(
            Grid(
                Label(f"\n{self.field_name}:"),
                input_field(self.value, self.field_type),
                Button("X", variant="error", id="clear", disabled = not self.field_optional),
                id = "field"
            ),
            Button("Confirmar", variant="primary", id="confirm"),
            Button("Cancelar", variant="error", id="cancel"),
            id="dialog",
        )


    @on(Input.Changed)
    def input_changed(self, event: Input.Changed):
        if self.value is None and event.value == "[VAZIO]":
            event.input.add_class("empty")
        elif self.value is None and event.value != "[VAZIO]":
            event.input.remove_class("empty")
            self.value = str(event.value)
        else:
            self.value = str(event.value)

        self.query_one("#confirm").disabled = not event.input.is_valid

    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        action = event.button.id

        if action == "confirm":
            if self.field_type == "date":
                self.value = datetime.strptime(self.value, '%Y-%m-%d')
            elif self.field_type == "integer":
                self.value = int(self.value)

            self.dismiss((self.field_name, self.value))
        elif action == "cancel":
            self.dismiss("cancel")
        else: # action == "clear"
            input = self.query_one(Input)
            input.value = "[VAZIO]"
            self.value = None

