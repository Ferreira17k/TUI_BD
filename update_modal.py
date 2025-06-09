from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.containers import Grid
from textual.widgets import Label, Button, Input


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

    #field-value {
        width: 100%;
    }

    #field-value.empty {
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


    def __init__(self, field_name: str, field_type, old_value):
        self.field_name = field_name
        self.field_type = field_type
        self.old_value = old_value
        self.value = old_value
        super().__init__()


    def compose(self) -> ComposeResult:
        yield Grid(
            Grid(
                Label(f"\n{self.field_name}:"),
                Input(self.old_value, placeholder="Novo valor", id="field-value"),
                Button("X", variant="error", id="clear"),
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

    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        action = event.button.id

        if action == "confirm":
            self.dismiss(self.value)
        elif action == "cancel":
            self.dismiss(None)
        else: # action == "clear"
            input = self.query_one("#field-value")
            input.value = "[VAZIO]"
            self.value = None

