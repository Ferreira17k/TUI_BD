from textual import on
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Label, Input, Select
from textual.containers import Vertical, Horizontal
import crud
from confirmation_dialog import ConfirmationDialog


TABLE_NAMES = ["experience", "experiencepicture", "review", "reviewpicture", "schedule", "subtypeexperience", "subtypeexperiencecategorizesexperience", "userprofile"]


def read_file(path):
    with open(path, "r") as f:
        return f.read()


class TableApp(App):
    CSS_PATH = "TableApp.css"

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label(read_file("ascii_art.txt"), id="title"),
            Horizontal(
                Label("\nSELECT * FROM "),
                Select.from_values(TABLE_NAMES),
                Label("\n WHERE "),
                Input(placeholder="Escreva seu filtro aqui", id="where-input")
            ),
            id = "vertical-1"
        )
        yield Label(read_file("tutor.txt"), id="tutor")
        yield DataTable()


    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = "cell"
        self.info = None
        self.cur_table = None


    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        self.cur_table = str(event.value)

    
    def delete_row(self, res):
        if res == "yes":
            table = self.query_one(DataTable)

            row_id = int(table.get_row_at(table.cursor_row)[0])               
           
            try:
                rows_deleted = crud.delete(self.cur_table, row_id)
                self.notify(f"{rows_deleted} linhas deletadas")
            except Exception as e:
                self.notify(str(e), severity="error", timeout=7)
            
            cursor_pos = table.cursor_coordinate
            self.query_bd()
        
            # reset cursor selection
            table.cursor_type = "cell"
            table.cursor_coordinate = cursor_pos


    def query_bd(self):
        table = self.query_one(DataTable)
        where = self.query_one("#where-input")

        query = f"SELECT * FROM {self.cur_table}"
        if where.value != "":
            query += " WHERE " + where.value

        if not self.info:
            self.info = crud.get_info()

        try:
            query_result = crud.select(query)

            table.clear(columns=True)  # Limpa colunas e dados
            table.add_columns(*[e[0] for e in self.info[self.cur_table]])
            table.add_rows(query_result)
        except Exception as e:
            self.notify(str(e), severity="error", timeout=7)
        

    async def on_key(self, event):
        table = self.query_one(DataTable)
    
        if event.key == "r":
            self.notify("Buscando resultados...", timeout=1)
            self.query_bd()
   
        elif event.key == "d":
            table.cursor_type = "row"  
            self.push_screen(
                ConfirmationDialog(
                    "Tem certeza de que quer deletar a linha?",
                    "Sim",
                    "Não"
                ),
                self.delete_row
            )

        elif event.key == "x":
            table.cursor_type = "column"

        elif event.key == "q":
            self.exit()
                                        
   
if __name__ == "__main__":
    app = TableApp()
    app.run()

