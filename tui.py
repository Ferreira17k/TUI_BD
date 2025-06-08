from textual.app import App, ComposeResult
from textual.widgets import DataTable, Label, Input
from textual.containers import Vertical
from textual import work

from confirmation_dialog import ConfirmationDialog


def read_file(path):
    with open(path, "r") as f:
        return f.read()


class TableApp(App):
    CSS = """
    Screen {
        align: center middle;
        layers: content hint;
    }

    Vertical {
        layer: content;
        width: 80%;
        height: auto;
        grid-gutter: 1;
        layout: grid;
    }

    #title {
        color: yellow;
        width: 100%;
        min-width: 100;
        content-align: center middle;
    }

    #tutor {
        layer: hint;
        width: 100%;
        position: absolute;
        content-align: right top;
        color: gray;
    }

    DataTable {
        margin-top: 2;
        content-align: center middle;
        height: 20;
        width: 80%;
        layer: content;
    }
    """


    def compose(self) -> ComposeResult:
        yield Label(read_file("tutor.txt"), id="tutor")
        yield Vertical(
            Label(read_file("ascii_art.txt"), id="title"),
            Input(placeholder="Escreva a sua query SQL aqui", id="main-input"),
        )
        yield DataTable()


    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_column("cupinto")


        self.push_screen(
            ConfirmationDialog(
                "Tem certeza de que quer deletar a linha?",
                "Sim",
                "Não"
            ),
            lambda res: table.add_row((res,))
        )


if __name__ == "__main__":
    app = TableApp()
    app.run()

