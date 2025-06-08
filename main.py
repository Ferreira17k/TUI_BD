from textual.app import App, ComposeResult
from textual.widgets import DataTable, Label, Input
from textual.containers import Vertical
import crud

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


    def make_table(self, select="select * from experience;"):
        conn = crud.get_connection()
        cur = conn.cursor()
        data_table = []

        cur.execute(select)
        resultados = cur.fetchall()
        data_table.extend(resultados)

        cur.close()
        conn.close()
        return data_table

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = 'cell'
    
    def delete_row(self, res):
        if res == "yes":
            
            table = self.query_one(DataTable)
            selected_row = table.get_row_at(table.cursor_row)
            row_id = int(selected_row[0])               
            
            coord = table.cursor_coordinate
            table.clear(columns=True)  
            dtable = self.make_table()
                        
            if dtable:
                table.add_columns(*[f"Column {i+1}" for i in range(len(dtable[0]))])
                table.add_rows(dtable)
        
            self.confirming_delete = False
            table.cursor_type = 'cell'

            table.cursor_coordinate = coord

            crud.delete("experience", row_id)
        
    def on_key(self, event):
        table = self.query_one(DataTable)
    
        if event.key == "1":
            dtable = self.make_table()
            table.clear(columns=True)  # Limpa colunas e dados
            if dtable:
                table.add_columns(*[f"Column {i+1}" for i in range(len(dtable[0]))])
                table.add_rows(dtable)
    
        elif event.key == "d":
            self.confirming_delete = True
            table.cursor_type = "row"  
            self.push_screen(
                ConfirmationDialog(
                    "Tem certeza de que quer deletar a linha?",
                    "Sim",
                    "Não"
                ),
                self.delete_row
            )
                                        
   


if __name__ == "__main__":
    app = TableApp()
    app.run()

