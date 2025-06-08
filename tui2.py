
from textual.app import App, ComposeResult
from textual.widgets import DataTable, _data_table
from connect import *

class TableApp(App):


    def make_table(self, table):
        conn = get_connection()
        cur = conn.cursor()
        data_table = []
        select = "select * from " + table + ";"
        cur.execute(select)
        resultados = cur.fetchall()

        for linha in resultados:
            data_table.append(linha)
            
        cur.close()
        conn.close()

        return data_table
       
    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)

        dtable = self.make_table("experience")
        # table.add_columns(dtable())
        table.add_rows(dtable)


if __name__ == "__main__":
    app = TableApp()
    app.run()

