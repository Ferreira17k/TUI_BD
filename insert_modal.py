from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.containers import Grid, Horizontal, Vertical
from textual.validation import Validator
from textual.widgets import Label, Button, Input


class InsertModal(ModalScreen[list]):
    CSS = """
    InsertModal {
        align: center middle;
    }

    #dialog {
        grid-size: 2;
        grid-gutter: 1 2;
        grid-rows: auto auto auto;
        padding: 0 1;
        width: auto;
        height: auto;
        background: $surface;
    }
    
    #question {
        column-span: 2;
        content-align: center middle;
    }

    #columns {
        column-span: 2;
        content-align: center middle;
    }

    Button {
        width: 100%;
    }

    Input {
        width: 100%;
    }

    .field-pair {
        width: 100%;
        content-align: left middle;
    }

    .field-label {
        width: 30%;
    }

    .field-input {
        width: 70%;
    }
    """
    

    def __init__(self, message: str, btn_yes: str, btn_no: str, info: dict):
        self.message = message
        self.btn_yes = btn_yes
        self.btn_no = btn_no
        self.info = info
        self.inputs: list[Input] = []  
        super().__init__()
    

    def compose(self) -> ComposeResult:

        self.column_names  = [e[0] for e in self.info] # lista de strings dos nomes das colunas
        self.column_types = [e[1] for e in self.info] # lista dos tipos das variáveis
        self.column_options = [e[2] for e in self.info] # True = opcional False = obrigatório
        
        field_pairs = []
        for name, optional, type in zip(self.column_names, self.column_options, self.column_types):
            label_text = f"{name} {'(opcional)' if optional else '*'}"
            input_field = Input(placeholder=f"Digite o valor ({type})...", classes="field-input")
            self.inputs.append(input_field)
            field_pairs.append(
                Horizontal(
                    Label(label_text, classes="field-label"),
                    input_field,
                    classes="field-pair"
                )
            )


        yield Grid(
            Label(self.message, id="question"),
            Vertical(*field_pairs, id="columns"),
            Button(self.btn_yes, variant="error", id="yes"),
            Button(self.btn_no, variant="primary", id="no"),
            id="dialog",
        )
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "yes":
            valores = []
    
            for input_field, tipo in zip(self.inputs, self.column_types):
                raw_value = input_field.value.strip()
    
                if tipo == "integer":
                    valores.append(int(raw_value))
                else:
                    valores.append(raw_value)

            self.dismiss(valores)
   
        else:
            self.dismiss(["no"])
