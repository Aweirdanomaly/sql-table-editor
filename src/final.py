import customtkinter
from PIL import Image


#table imports
import sys

#from PySide6.QtCore import Qt, QSortFilterProxyModel, QAbstractTableModel
from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableView
)



customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"



class SQLEditor(customtkinter.CTk):
    def __init__(self):
        super().__init__()
    
        
        # configure window
        self.title("SQL Editor")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=10, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)
        
#         self.logo_img = customtkinter.CTkImage(Image.open("./business.png"), size=(100, 50))
#         self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="SQL Editor", font=customtkinter.CTkFont(size=15, weight="bold"), image=self.logo_img, compound="left")
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="SQL Editor", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))    

        
        self.host = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="host")
        self.host.grid(row=1, column=0, columnspan=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.user = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="user")
        self.user.grid(row=2, column=0, columnspan=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.password = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="password")
        self.password.grid(row=3, column=0, columnspan=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.database = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="database")
        self.database.grid(row=4, column=0, columnspan=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.driver_optionmenu= customtkinter.CTkOptionMenu(self.sidebar_frame, dynamic_resizing=False,
                                                        values=["SQLite", "MySQL", "ODBC", "PostgresSQL", "MariaDB"])
        self.drivers={"SQLite":"QSQLITE", "MySQL":"QMYSQL", "ODBC":"QODBC", "PostgresSQL":"QPSQL", "MariaDB":"QMARIADB"}
        self.driver_optionmenu.grid(row=5, column=0, padx=10, pady=5)
        self.connect_button = customtkinter.CTkButton(self.sidebar_frame, text="Connect", command=self.connect_db)
        self.connect_button.grid(row=6, column=0, padx=10, pady=5)

        
        #sidebar settings
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="sw")
        self.appearance_mode_label.grid(row=8, column=0, padx=20, pady=(10, 0), sticky="s")
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["System", "Light", "Dark"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 10), sticky="s")
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="sw")
        self.scaling_label.grid(row=10, column=0, padx=20, pady=(10, 0), sticky="s")
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=11, column=0, padx=20, pady=(10, 20), sticky="s")

        
        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Search Strings")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Search", command=self.display_table)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox and tabs
        self.textbox = customtkinter.CTkTextbox(self, width=500)
        self.textbox.grid(row=0, rowspan=3 , column=1, columnspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.textbox = customtkinter.CTkTextbox(self, width=500)
        self.textbox.grid(row=0, rowspan=3 , column=1, columnspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew")

        
        #div
#         # create textbox and tabs
#         self.tabview = customtkinter.CTkTabview(self, width=500)
#         self.tabview.grid(row=0, rowspan=4, column=1, columnspan=4, padx=(20, 20), pady=(20, 10), sticky="nsew")
#         self.tabview.add("SQL Editor")
#         self.tabview.add("Tab 2")
#         self.tabview.add("Tab 3")
        
#         self.textbox = customtkinter.CTkTextbox(self.tabview.tab("SQL Editor"))
#         self.textbox.pack(padx=20, pady=20)
#         #self.textbox.grid(row=0, rowspan=5 , column=1, columnspan=5, padx=(20, 20), pady=(20, 0), sticky="nsew")
        
#         self.entry = customtkinter.CTkEntry(self.tabview.tab("SQL Editor"), placeholder_text="Search Strings")
#         self.entry.pack(padx=20, pady=20)
#         #self.entry.grid(row=3, column=1, columnspan=10, padx=(20, 0), pady=(20, 20), sticky="nsew")
#         self.main_button_1 = customtkinter.CTkButton(self.tabview.tab("SQL Editor"), fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Search")
#         self.main_button_1.pack(padx=20, pady=20)
#         #self.main_button_1.grid(row=3, column=5, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
    def display_table(self):
        if hasattr(self, 'col_boxes') ==False:
            self.Popup("You did not select a table")

        bitmap=[x.get() for x in self.col_boxes]
        record = self.qt_win.model.record()
        for idx, el in enumerate(bitmap):
            if el==0:
                self.qt_win.view.hideColumn(idx)
        self.column_names = [record.fieldName(i) for i in range(record.count())]
        string=self.entry.get()
        if string!="":
            self.match_strings(string)
        self.qt_win.show()
        
        self.qt_app.exec()
    
    
    def match_strings(self, s):
        w="||' '||".join(self.column_names)
        query = QSqlQuery(self.con)
        query.prepare(f"""SELECT * FROM {self.table} WHERE ({w}) LIKE '%{s}%'""")
        query.exec()
        self.qt_win.model.setQuery(query)
    
    
    def connect_db(self):
        #debug command to find path to drivers installed 
        #print(f"here's the driver path': {self.drivers[self.driver_optionmenu.get()]} {self.driver_optionmenu.get()}")
        
        self.con = QSqlDatabase.addDatabase(self.drivers[self.driver_optionmenu.get()])
        self.con.setDatabaseName(self.database.get())
        self.con.setHostName(self.host.get())
        self.con.setUserName(self.user.get())
        self.con.setPassword(self.password.get())
        
        # self.con = QSqlDatabase.addDatabase("QSQLITE")
        # self.con.setDatabaseName("chinook.db")
        # self.con.setHostName("")
        # self.con.setUserName("root")
        # self.con.setPassword("root")
        if not self.con.open():
            self.Popup(f"Could not connect to table due to the following error:\n{self.con.lastError().databaseText()}")
        else:
            self.show_tables()
        


    def show_tables(self):
        self.options = customtkinter.CTkToplevel(self)
        self.options.geometry("1600x800")
        
        self.tables_frame = customtkinter.CTkFrame(self.options)
        self.tables_frame.pack(padx=10, pady=10)
        
        self.table_buttons=[customtkinter.CTkButton(master=self.tables_frame, text=x, command=lambda j=x: self.get_table(j)) for x in self.con.tables()]
        for idx,btn in enumerate(self.table_buttons):
            btn.grid(row=idx // 3, column=idx % 3, pady=(20, 10), padx=20, sticky="n")
        
        
    def get_table(self, text):
        self.table=str(text)
        if not QApplication.instance():
            self.qt_app = QApplication(sys.argv)
        else:
            self.qt_app = QApplication.instance()
        self.qt_win = Contacts(self.table)
        record = self.qt_win.model.record()
        self.column_names = [record.fieldName(i) for i in range(record.count())]
        self.show_columns(self.column_names)

        
    def show_columns(self, cols):
        if hasattr(self, 'cols_frame'):
            try:
                for widget in self.cols_frame.winfo_children():
                    widget.destroy()
            except:
                self.cols_frame = customtkinter.CTkFrame(self.options)
                self.cols_frame.pack(padx=10, pady=10)
        else:
            self.cols_frame = customtkinter.CTkFrame(self.options)
            self.cols_frame.pack(padx=10, pady=10)
        self.col_boxes=[customtkinter.CTkCheckBox(master=self.cols_frame, text=x) for x in cols]
        for idx,box in enumerate(self.col_boxes):
            box.select()
            box.grid(row=idx // 3, column=idx % 3, pady=(20, 10), padx=20, sticky="n")
        
        
    def Popup(self, t):
        popup = customtkinter.CTkToplevel(self)
        popup.geometry("400x200")

        # create label on CTkToplevel window
        label = customtkinter.CTkLabel(popup, text=t)
        label.pack(side="top", fill="both", expand=True, padx=40, pady=40)
        
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    
class Contacts(QMainWindow):
    def __init__(self, table, parent=None):
        super().__init__(parent)
        self.setWindowTitle("QTableView Example")
        self.resize(800, 500)
        # Set up the model
        self.model = QSqlTableModel(self)
        self.model.setTable(table)
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)

        
        self.model.select()
        # Set up the view
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.resizeColumnsToContents()
        
        self.setCentralWidget(self.view)


if __name__ == "__main__":
    app = SQLEditor()
    app.mainloop()
    
    