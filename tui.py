from textual.app import App, ComposeResult
from textual.widgets import DataTable

class TableApp(App):
    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("Name", "Age", "City")
        table.add_rows(
            [
                ("Alice", "30", "New York"),
                ("Bob", "25", "Los Angeles"),
                ("Charlie", "35", "Chicago"),
            ]
        )


if __name__ == "__main__":
    app = TableApp()
    app.run()

