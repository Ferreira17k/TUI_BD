from textual.app import App, ComposeResult
from textual.widgets import DataTable, Label
from textual.containers import Vertical
from confirmation_dialog import *
from connect import *
import crud

class TableApp(App):

    def __init__(self):
        super().__init__()
        self.confirming_delete = False
     
    def make_table(self, select="select * from experience;"):
        conn = get_connection()
        cur = conn.cursor()
        data_table = []

        cur.execute(select)
        resultados = cur.fetchall()
        data_table.extend(resultados)

        cur.close()
        conn.close()
        return data_table

    def compose(self) -> ComposeResult:
        yield DataTable()

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
    
        elif event.key == "d" and not self.confirming_delete:
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

                                           
        elif event.key == "n" and self.confirming_delete:
            self.confirming_delete = False
            table.cursor_type = 'cell'

if __name__ == "__main__":
    app = TableApp()
    app.run()
   
