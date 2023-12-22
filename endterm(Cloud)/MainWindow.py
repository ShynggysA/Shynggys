import base64
import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from AuthorizationWindow import AuthorizationWindow

class DatabaseManager:
    def __init__(self):
        self.conn_users = sqlite3.connect('users.db')
        self.conn_files = sqlite3.connect('files.db')
        self.conn_basket_files = sqlite3.connect('basket_files.db')

    def create_user_table(self):
        cursor = self.conn_users.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                email TEXT,
                password_hash TEXT,
                salt TEXT
            )
        ''')
        self.conn_users.commit()

    def create_files_table(self):
        cursor = self.conn_files.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                content TEXT,
                user_email TEXT,
                favorite TEXT
            )
        ''')
        self.conn_files.commit()

    def create_basket_files(self):
        cursor = self.conn_basket_files.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS basket_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                content TEXT,
                user_email TEXT
            )
        ''')
        self.conn_basket_files.commit()

    def save_file(self, filename, encoded_content, email, favorite):
        cursor = self.conn_files.cursor()
        cursor.execute('INSERT INTO files (filename, content, user_email, favorite) VALUES (?, ?, ?, ?)', (filename, encoded_content, email, favorite))
        self.conn_files.commit()

    def get_files_by_user(self, email):
        cursor = self.conn_files.cursor()
        cursor.execute('SELECT filename FROM files WHERE user_email=?', (email,))
        files = cursor.fetchall()
        return files
    
    def get_basket_files_by_user(self, email):
        cursor = self.conn_basket_files.cursor()
        cursor.execute('SELECT filename FROM basket_files WHERE user_email=?', (email,))
        files = cursor.fetchall()
        return files
    
    def get_favorite_files_by_user(self, email):
        cursor = self.conn_files.cursor()
        cursor.execute('SELECT filename FROM files WHERE user_email=? AND favorite=?', (email, 'True'))
        files = cursor.fetchall()
        return files

class MainCloudWindow:
    def __init__(self, root, authorization_window, email, username):
        self.authorization_window = authorization_window
        self.email = email
        self.username = username
        self.root = root
        self.root.title("Облочное хралнилще")
        self.root.geometry("600x450")

        self.db_manager = DatabaseManager()
        self.db_manager.create_user_table()
        self.db_manager.create_files_table()
        self.db_manager.create_basket_files()

        self.tab_control = ttk.Notebook(self.root)

        self.create_tabs()
        self.authorization_window.destroy()
        self.tab_control.bind("<<NotebookTabChanged>>", self.update_file_list)

    def show_tab(self, event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")

    def create_tabs(self):
        self.tab_control = ttk.Notebook(self.root)

        personal_tab = PersonalTab(self.tab_control, db_manager=self.db_manager, username=self.username, email=self.email)
        all_files_tab = AllFilesTab(self.tab_control, db_manager=self.db_manager, username=self.username, email=self.email)
        favorites_tab = FavoritesTab(self.tab_control, db_manager=self.db_manager, username=self.username, email=self.email)
        trash_tab = TrashTab(self.tab_control, db_manager=self.db_manager, username=self.username, email=self.email)

        self.tab_control.add(personal_tab, text="Личный кабинет")
        self.tab_control.add(all_files_tab, text="Все файлы")
        self.tab_control.add(favorites_tab, text="Избранное")
        self.tab_control.add(trash_tab, text="Корзина")

        self.tab_control.pack(expand=1, fill="both")

        self.tab_control.bind("<<NotebookTabChanged>>", self.show_tab)

    def update_file_list(self, event):
        selected_tab = event.widget.select()
        tab_index = event.widget.index(selected_tab)

        current_tab = self.tab_control.winfo_children()[tab_index]

        if hasattr(current_tab, 'add_file_list'):
            current_tab.add_file_list()

class PersonalTab(ttk.Frame):
    def __init__(self, master=None, db_manager=None, auth_window=None, username="", email="", **kwargs):
        super().__init__(master, **kwargs)
        self.main_cloud_window = MainCloudWindow
        self.db_manager = db_manager
        self.auth_window = auth_window

        self.label_name = Label(self, text=f"Имя: {username}", font='Arial 13 bold', fg='black')
        self.label_name.place(x=180, y=80)

        self.label_email = Label(self, text=f"Эл.почта: {email}", font='Arial 13 bold', fg='black')
        self.label_email.place(x=180, y=120)

        self.logout_btn = Button(self, text='Выйти', font='Arial 10 bold', command=self.logout)
        self.logout_btn.place(x=250, y=160)

    def logout(self):
        self.master.master.destroy()
        new_auth_window = AuthorizationWindow()
        new_auth_window.protocol("WM_DELETE_WINDOW", new_auth_window.on_close)
        new_auth_window.mainloop()

    def on_close(self):
        self.master.deiconify()
        self.root.destroy()

class AllFilesTab(ttk.Frame):
    def __init__(self, master=None, db_manager=None, username="", email="", **kwargs):
        super().__init__(master, **kwargs)

        self.db_manager = db_manager
        self.username = username
        self.email = email

        upload_button = tk.Button(self, text="Выбрать файл", command=self.upload_file)
        upload_button.pack(pady=5)

        self.file_listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.file_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        delete_button = tk.Button(self, text="Добавить в Избранное", command=self.add_favorite)
        delete_button.place(x=130, y=380)

        download_button = tk.Button(self, text="Скачать", command=self.download_file)
        download_button.place(x=280, y=380)
        
        delete_button = tk.Button(self, text="Удалить", command=self.move_basket)
        delete_button.place(x=350, y=380)
        
        self.file_listbox.bind("<<ListboxSelect>>", self.on_file_select)

        self.add_file_list()
            
    def upload_file(self):
        file_path = filedialog.askopenfilename(title="Выберите файл")

        if file_path:
            with open(file_path, 'rb') as file:
                file_content = file.read()

            filename = file_path.split("/")[-1]
            encoded_content = base64.b64encode(file_content).decode('utf-8')
            favorite = 'False'

            self.db_manager.save_file(filename, encoded_content, self.email, favorite)

            self.add_file_list()

            messagebox.showinfo("Загрузка файла", f"Файл {filename} успешно загружен.")

    def add_favorite(self):
        if hasattr(self, 'selected_file'):
            favorite = 'True'
            cursor = self.db_manager.conn_files.cursor()
            cursor.execute('UPDATE files SET favorite=? WHERE filename=? AND user_email=?', (favorite, self.selected_file, self.email))
            self.db_manager.conn_files.commit()

            messagebox.showinfo("Добавить в Избранное", f"Файл {self.selected_file} добавлен в Избранное." )

    def download_file(self):
        if hasattr(self, 'selected_file'):
            cursor = self.db_manager.conn_files.cursor()
            cursor.execute('SELECT filename, content FROM files WHERE filename=? AND user_email=?', (self.selected_file, self.email))
            file_info = cursor.fetchone()

            if file_info:
                filename, encoded_content = file_info
                decoded_content = base64.b64decode(encoded_content)

                file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All Files", "*.*")], initialfile=filename)
                if file_path:
                    with open(file_path, 'wb') as file:
                        file.write(decoded_content)

                messagebox.showinfo("Скачять файл", f"Файл {self.selected_file} успешно скачано.")

    def move_basket(self):
        if hasattr(self, 'selected_file'):
            result = messagebox.askquestion("Удаление файла", f"Вы уверены, что хотите удалить файл {self.selected_file}?")

            if result == "yes":
                cursor = self.db_manager.conn_files.cursor()
                cursor.execute('SELECT filename, content FROM files WHERE filename=? AND user_email=?', (self.selected_file, self.email))
                file_info = cursor.fetchone()

                filename, encoded_content = file_info
                cursor = self.db_manager.conn_basket_files.cursor()
                cursor.execute('INSERT INTO basket_files (filename, content, user_email) VALUES (?, ?, ?)', (filename, encoded_content, self.email))
                self.db_manager.conn_basket_files.commit()

                cursor = self.db_manager.conn_files.cursor()
                cursor.execute('DELETE FROM files WHERE filename=? AND user_email=?', (self.selected_file, self.email))
                self.db_manager.conn_files.commit()

                self.add_file_list()

                messagebox.showinfo("Удаление файла", f"Файл {self.selected_file} успешно удален.")

    def on_file_select(self, event):
        selected_item = self.file_listbox.curselection()
        if selected_item:
            self.selected_file = self.file_listbox.get(selected_item)

    def add_file_list(self):
        files = self.db_manager.get_files_by_user(self.email)
        self.file_listbox.delete(0, 'end')
        for file in files:
            self.file_listbox.insert(0, file[0])

class FavoritesTab(ttk.Frame):
    def __init__(self, master=None, db_manager=None, username="", email="", **kwargs):
        super().__init__(master, **kwargs)

        self.db_manager = db_manager
        self.username = username
        self.email = email

        self.file_listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.file_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        download_button = tk.Button(self, text="Скачать", command=self.download_file)
        download_button.place(x=210, y=380)
        
        delete_button = tk.Button(self, text="Удалить из Избранных", command=self.delete_favorites)
        delete_button.place(x=280, y=380)

        self.file_listbox.bind("<<ListboxSelect>>", self.on_file_select)

        self.add_file_list()

    def on_file_select(self, event):
        selected_item = self.file_listbox.curselection()
        if selected_item:
            self.selected_file = self.file_listbox.get(selected_item)

    def download_file(self):
        if hasattr(self, 'selected_file'):
            cursor = self.db_manager.conn_files.cursor()
            cursor.execute('SELECT filename, content FROM files WHERE filename=? AND user_email=?', (self.selected_file, self.email))
            file_info = cursor.fetchone()

            if file_info:
                filename, encoded_content = file_info
                decoded_content = base64.b64decode(encoded_content)

                file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All Files", "*.*")], initialfile=filename)
                if file_path:
                    with open(file_path, 'wb') as file:
                        file.write(decoded_content)

                messagebox.showinfo("Скачять файл", f"Файл {self.selected_file} успешно скачано.")

    def delete_favorites(self):
        if hasattr(self, 'selected_file'):
            result = messagebox.askquestion("Удаление из Избранных", f"Вы уверены, что хотите удалить файл {self.selected_file}?")

            if result == "yes":
                favorite = 'False'
                cursor = self.db_manager.conn_files.cursor()
                cursor.execute('UPDATE files SET favorite=? WHERE filename=? AND user_email=?', (favorite, self.selected_file, self.email))
                self.db_manager.conn_files.commit()

                self.add_file_list()

                messagebox.showinfo("Удаление файла", f"Файл {self.selected_file} успешно удален из Избранных.")

    def add_file_list(self):
        files = self.db_manager.get_favorite_files_by_user(self.email)
        self.file_listbox.delete(0, 'end')
        for file in files:
            self.file_listbox.insert(0, file[0])

class TrashTab(ttk.Frame):
    def __init__(self, master=None, db_manager=None, username="", email="", **kwargs):
        super().__init__(master, **kwargs)

        self.db_manager = db_manager
        self.username = username
        self.email = email

        self.file_listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.file_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        download_button = tk.Button(self, text="Восстановить", command=self.restore_file)
        download_button.place(x=210, y=380)
        
        delete_button = tk.Button(self, text="Удалить", command=self.delete_file)
        delete_button.place(x=320, y=380)

        self.file_listbox.bind("<<ListboxSelect>>", self.on_file_select)

        self.add_file_list()

    def on_file_select(self, event):
        selected_item = self.file_listbox.curselection()
        if selected_item:
            self.selected_file = self.file_listbox.get(selected_item)

    def restore_file(self):
        if hasattr(self, 'selected_file'):
            result = messagebox.askquestion("Восстановлени файла", f"Вы уверены, что хотите восстановить файл {self.selected_file}?")

            if result == "yes":
                cursor = self.db_manager.conn_basket_files.cursor()
                cursor.execute('SELECT filename, content FROM basket_files WHERE filename=? AND user_email=?', (self.selected_file, self.email))
                file_info = cursor.fetchone()

                filename, encoded_content = file_info
                cursor = self.db_manager.conn_files.cursor()
                cursor.execute('INSERT INTO files (filename, content, user_email) VALUES (?, ?, ?)', (filename, encoded_content, self.email))
                self.db_manager.conn_files.commit()

                cursor = self.db_manager.conn_basket_files.cursor()
                cursor.execute('DELETE FROM basket_files WHERE filename=? AND user_email=?', (self.selected_file, self.email))
                self.db_manager.conn_basket_files.commit()

                self.add_file_list()

                messagebox.showinfo("Восстановление файла", f"Файл {self.selected_file} успешно восстановлен.")

    def delete_file(self):
        if hasattr(self, 'selected_file'):
            result = messagebox.askquestion("Удаление файла", f"Вы уверены, что хотите удалить файл {self.selected_file}?")

            if result == "yes":
                cursor = self.db_manager.conn_basket_files.cursor()
                cursor.execute('DELETE FROM basket_files WHERE filename=? AND user_email=?', (self.selected_file, self.email))
                self.db_manager.conn_basket_files.commit()

                self.add_file_list()

                messagebox.showinfo("Удаление файла", f"Файл {self.selected_file} успешно удален.")

    def add_file_list(self):
        files = self.db_manager.get_basket_files_by_user(self.email)
        self.file_listbox.delete(0, 'end')
        for file in files:
            self.file_listbox.insert(0, file[0])

if __name__ == "__main__":
    root = tk.Tk()
    app = AuthorizationWindow()
    root.mainloop()
