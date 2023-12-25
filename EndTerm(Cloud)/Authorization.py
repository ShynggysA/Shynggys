import os
import hashlib
import sqlite3
import logging
import requests
import tkinter as tk
from config import API_KEY
from tkinter import *
from tkinter import messagebox
from time import strftime
from email_validator import validate_email, EmailNotValidError

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s', encoding='utf-8')

class DatabaseManager:
    def __init__(self, connection):
        self.conn = connection
        logging.info('DatabaseManager инициализирован для AuthorizationWindow')

    def create_user_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                email TEXT,
                password_hash TEXT,
                salt TEXT
            )
        ''')
        self.conn.commit()
        logging.info('Таблица пользователей создана')

    def check_account_details(self, email, password):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email=?', (email,))
        user = cursor.fetchone()

        if user:
            stored_salt = bytes.fromhex(user[4])
            hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), stored_salt, 100000).hex()
            return hashed_password == user[3]
        else:
            return None
        
        logging.info('Учетные данные проверены')

    def save_account_details(self, username, email, password):
        salt = os.urandom(32)
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO users (username, email, password_hash, salt) VALUES (?, ?, ?, ?)',
                       (username, email, hashed_password, salt.hex()))
        self.conn.commit()
        logging.info('Учетные данные пользователя сохранены')

    def check_email_exists(self, email):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email=?', (email,))
        user = cursor.fetchone()
        return user is not None
        logging.info('Поля для ввода проверены')
    
    def get_user_info(self, email):
        cursor = self.conn.cursor()
        cursor.execute('SELECT username, email FROM users WHERE email=?', (email,))
        user_info = cursor.fetchone()
        return user_info
        logging.info('Учетные данные пользователя получены')

class RealTimeClock(tk.Label):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self['font'] = 'Helvetica 12'
        self.update_time()

    def get_current_time(self, api_key, timezone):
        url = f'http://api.timezonedb.com/v2.1/get-time-zone'
        params = {'key': api_key, 'format': 'json', 'by': 'zone', 'zone': timezone}
        
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            current_time = data['formatted']
            return current_time.split()[1][:5]

    def update_time(self):
        api_key = API_KEY
        timezone = 'Asia/Almaty'

        current_time = self.get_current_time(api_key, timezone)
        self['text'] = current_time

        self.after(1000, self.update_time)

class AuthorizationWindow(Tk):
    def __init__(self):
        super().__init__()

        self.title('Авторизацияция')
        self.geometry('600x450')
        self.resizable(width=False, height=False)
        self['bg'] = 'white'

        self.db_manager = DatabaseManager(sqlite3.connect('users.db'))
        self.db_manager.create_user_table()

        self.frames = {
            'signin': SignInFrame(self),
            'login': LogInFrame(self)
        }

        self.show_frame('login')

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.pack(fill=BOTH, expand=YES)
        frame.tkraise()

        if frame_name == 'personal':
            frame.show_user_info(self.email_entry.get().lower())

    def open_main_window(self,username, email):
        from MainWindow import MainCloudWindow
        root = tk.Tk()
        main_window = MainCloudWindow(root, self, email, username)
        root.mainloop()

    def on_close(self):
        self.db_manager.conn.close()
        self.destroy()

class LogInFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.clock_label = RealTimeClock(self)
        self.clock_label.place(x=540, y=5)

        main_label = Label(self, text='Авторизация', font='Arial 19 bold', fg='black')
        main_label.place(x=225, y=25)

        email_label = Label(self, text='Эл.почта', font='Arial 13 bold', fg='black')
        email_label.place(x=180, y=100)

        self.email_entry = Entry(self, bg='white', fg='black', font='Arial 13', width=25)
        self.email_entry.bind('<Return>', self.confirm)
        self.email_entry.place(x=175, y=125)

        password_label = Label(self, text='Пароль', font='Arial 13 bold', fg='black')
        password_label.place(x=180, y=180)

        self.password_entry = Entry(self, bg='white', fg='black', font='Arial 13', width=25, show='\u2022')
        self.password_entry.bind('<Return>', self.confirm)
        self.password_entry.place(x=175, y=205)

        self.show_password_var = IntVar()
        show_password_checkbox = Checkbutton(self, text='Показать пароль', font='Arial 9', variable=self.show_password_var, command=self.password_visibility)
        show_password_checkbox.place(x=180, y=235)

        confirm_btn = Button(self, text='Войти', font='Arial 10 bold', command=self.confirm)
        confirm_btn.place(x=280, y=280)

        registration_btn = Button(self, text='Регистрация', font='Arial 10 bold', command=self.registration)
        registration_btn.place(x=260, y=315)

    def password_visibility(self):
        if self.show_password_var.get():
            self.password_entry['show'] = ''
        else:
            self.password_entry['show'] = '\u2022'

    def check_entry_fields_login(self):
        return bool(self.email_entry.get() and self.password_entry.get())

    def confirm(self, event=None):
        email = self.email_entry.get().lower()
        password = self.password_entry.get()
        
        if not self.check_entry_fields_login():
            messagebox.showwarning('Предупреждение', 'Введите почту и пароль')
            return
        elif self.master.db_manager.check_account_details(email, password):
            user_info = self.master.db_manager.get_user_info(email)
            if user_info:
                username, email = user_info
                messagebox.showinfo('Вход', f'Здравствуйте, {username}. Вы успешно вошли')
                self.master.open_main_window(username, email)
            else:
                messagebox.showwarning('Внимание', 'Не удалось получить информацию о пользователе')
        else:
            messagebox.showerror('Ошибка', 'Неправильный логин или пароль')

    def registration(self):
        self.pack_forget()
        self.master.show_frame('signin')

class SignInFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.clock_label = RealTimeClock(self)
        self.clock_label.place(x=540, y=5)

        main_label = Label(self, text='Регистрация', font='Arial 19 bold', fg='black')
        main_label.place(x=225, y=25)

        username_label = Label(self, text='Имя', font='Arial 13 bold', fg='black')
        username_label.place(x=180, y=80)

        self.username_entry = Entry(self, bg='white', fg='black', font='Arial 13', width=25)
        self.username_entry.bind('<Return>', self.registration)
        self.username_entry.place(x=175, y=105)

        email_label = Label(self, text='Эл.почта', font='Arial 13 bold', fg='black')
        email_label.place(x=180, y=140)

        self.email_entry = Entry(self, bg='white', fg='black', font='Arial 13', width=25)
        self.email_entry.bind('<Return>', self.registration)
        self.email_entry.place(x=175, y=165)

        password1_label = Label(self, text='Пароль', font='Arial 13 bold', fg='black')
        password1_label.place(x=180, y=200)

        self.password1_entry = Entry(self, bg='white', fg='black', font='Arial 13', width=25, show='\u2022')
        self.password1_entry.bind('<Return>', self.registration)
        self.password1_entry.place(x=175, y=225)

        password2_label = Label(self, text='Повторите пароль', font='Arial 13 bold', fg='black')
        password2_label.place(x=180, y=260)

        self.password2_entry = Entry(self, bg='white', fg='black', font='Arial 13', width=25, show='\u2022')
        self.password2_entry.bind('<Return>', self.registration)
        self.password2_entry.place(x=175, y=285)

        self.show_password_var = IntVar()
        show_password_checkbox = Checkbutton(self, text='Показать пароль', font='Arial 9', variable=self.show_password_var, command=self.password_visibility)
        show_password_checkbox.place(x=180 , y=310)

        registration_btn = Button(self, text='Зарегистрироваться', font='Arial 10 bold', command=self.registration)
        registration_btn.place(x=235, y=340)

        back_to_login = Button(self, text='Назад на страницу Входа', font='Arial 10 bold', command=self.login)
        back_to_login.place(x=215, y=375)

    def password_visibility(self):
        if self.show_password_var.get():
            self.password1_entry['show'] = ''
            self.password2_entry['show'] = ''
        else:
            self.password1_entry['show'] = '\u2022'
            self.password2_entry['show'] = '\u2022'

    def check_entry_fields_sigin(self):
        return bool(self.username_entry.get() and self.email_entry.get() and self.password1_entry.get() and self.password2_entry.get())

    def check_email(self):
        try:
            validate_email(self.email_entry.get(), check_deliverability=True)
            return True
        except EmailNotValidError as e:
            messagebox.showinfo('Ошибка', str(e))
            return False

    def check_passwords(self):
        return self.password1_entry.get() == self.password2_entry.get()

    def registration(self, event=None):
        email = self.email_entry.get().lower()
        password = self.password1_entry.get()
        username = self.username_entry.get()

        if not self.check_entry_fields_sigin():
            messagebox.showwarning('Предупреждение', 'Заполните все поля')
            return
        elif not self.check_email():
            return
        elif self.master.db_manager.check_email_exists(email):
            messagebox.showerror('Ошибка', 'Пользователь уже существует')
            return
        elif not self.check_passwords():
            messagebox.showerror('Ошибка', 'Пароли не совпадают или одно из полей пусто')
            return
        else:
            self.master.db_manager.save_account_details(username, email, password)
            messagebox.showinfo('Успешная регистрация', 'Вы успешно зарегистрировались')
            self.pack_forget()
            self.master.show_frame('login')

    def login(self):
        self.pack_forget()
        self.master.show_frame('login')

def on_close():
    app.db_manager.conn.close()
    app.destroy()

if __name__ == "__main__":
    app = AuthorizationWindow()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
