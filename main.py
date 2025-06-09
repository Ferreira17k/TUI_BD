from typing import cast
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Label, Input, Select
from textual.containers import Vertical, Horizontal
import crud
from insert_modal import InsertModal 
from confirmation_dialog import ConfirmationDialog
from update_modal import UpdateModal
from time import time


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
        self.table_not_empty = False
        self.modal_active = False


    @on(Select.Changed)
    def select_changed(self, event: Select.Changed):
        if event.value:
            self.cur_table = str(event.value)


    def modal_insert(self, values):

        if values[0] == "no":
            return
        else:
            dict = {}
            if self.info is None:
                self.info = crud.get_info()
                
            column_names = [e[0] for e in self.info[self.cur_table]]
            for key, value in zip(column_names ,values):
                dict[f'{key}'] = value

            try:
                rows_insert = crud.insert(self.cur_table, dict)
                self.notify(f"Linha inserida")
            except Exception as e:
                self.notify(str(e), severity="error", timeout=7)
            
            table = self.query_one(DataTable)
            self.query_bd(keep_scroll=True)
            
    
    def delete_row(self, res):
        self.modal_active = False

        self.query_one(DataTable).cursor_type = "cell"

        if res == "yes":
            table = self.query_one(DataTable)

            row_values = table.get_row_at(table.cursor_row)  
            columns = crud.get_columns(self.cur_table)  
            dicio = {}
            for index, column in enumerate(columns):
                dicio[column] = row_values[index]          
            try:
                crud.delete_2(self.cur_table, dicio)
                self.notify("1 linha deletadas")
            except Exception as e:
                self.notify(str(e), severity="error", timeout=7)
            
            self.query_bd(keep_scroll=True)


    def create_index(self, res):
        self.modal_active = False
        table = self.query_one(DataTable)

        if res == "yes":
            column_index = table.cursor_column
            column_name = crud.get_columns(self.cur_table)[column_index]
            try:
                crud.create_index(self.cur_table, column_names=[column_name], unique=True)
                self.notify(f"Índice criado para coluna '{column_name}'", severity="info")
            except Exception as e:
                self.notify(str(e), severity="error", timeout=7)
        
        table.cursor_type = "cell"


    def query_bd(self, keep_scroll=False):
        table = self.query_one(DataTable)
        where = cast(Select, self.query_one("#where-input"))

        if not self.info:
            self.info = crud.get_info()

        column_names = [e[0] for e in self.info[self.cur_table]]

        query = f"SELECT * FROM {self.cur_table}"
        if where.value != "":
            query += " WHERE " + str(where.value)

        query += " ORDER BY " + column_names[0]

        try:
            query_result = crud.select(query)

            scroll = table.scroll_offset
            cursor_pos = table.cursor_coordinate

            # Limpa o estado atual da tabela e o redefine
            table.clear(columns=True)
            table.add_columns(*column_names)
            table.add_rows(query_result)

            if keep_scroll:
                table.cursor_coordinate = cursor_pos
                table.set_scroll(scroll.x, scroll.y)

            self.table_not_empty = True
        except Exception as e:
            self.notify(str(e), severity="error", timeout=7)


    def update_cell(self, info):
        table = self.query_one(DataTable)

        self.modal_active = False

        if info == "cancel":
            return
        
        field_name, value = info
        id = int(table.get_row_at(table.cursor_row)[0])

        try:
            crud.update(self.cur_table, id, field_name, [value])
            self.query_bd(keep_scroll=True)
        except Exception as e:
            self.notify(str(e), severity="error", timeout=7)
        

    def on_key(self, event):
        table = self.query_one(DataTable)
    
        if event.key == "r":
            start = time()
            self.query_bd()
            self.notify(f"Tabela atualizada ({time() - start:.1f}s)", timeout=3)

        elif event.key == "u" and not self.modal_active:
            if self.table_not_empty:
                if self.cur_table == "subtypeexperiencecategorizesexperience" or \
                    table.cursor_column == 0: # ID

                    self.notify("Esse valor não pode ser modificado")
                    return

                col = self.info[self.cur_table][table.cursor_column]
                old_value = table.get_cell_at(table.cursor_coordinate)
                self.modal_active = True
                self.push_screen(
                    UpdateModal(col, str(old_value)),
                    self.update_cell
                )
   
        elif event.key == "d" and not self.modal_active:
            table.cursor_type = "row"
            self.modal_active = True
            self.push_screen(
                ConfirmationDialog(
                    "Tem certeza de que quer deletar a linha?",
                    "Sim", "Não"
                ),
                self.delete_row
            )

        elif event.key == "x":
            table.cursor_type = "column"
            self.modal_active = True
            self.push_screen(
                ConfirmationDialog(
                    "Tem certeza de que quer criar um índice?",
                    "Sim",
                    "Não"
                ),
                self.create_index
            )

        elif event.key == "q":
            self.exit()


        elif event.key == "i" and self.info is not None:
            self.push_screen(
                InsertModal(
                    "Tem certeza de que quer inserir a linha?",
                    "Sim",
                    "Não",
                    self.info[self.cur_table]
                ),
                self.modal_insert
            )
            
   
if __name__ == "__main__":
    app = TableApp()
    app.run()

