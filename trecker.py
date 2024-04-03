import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Устанавливаем тему оформления и цветовую схему
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class Application(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Учёт финансов")
        self.geometry(f"{800}x{500}")

        # настройка сетки расположения
        self.grid_columnconfigure(1, weight=5)
        self.grid_rowconfigure(0, weight=5)

        self.income = 0
        self.expense = 0
        self.income_transactions = []
        self.expense_transactions = []

        # создание главного фрейма
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # создание боковой панели с виджетами
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Учёт финансов",
                                       font=ctk.CTkFont(size=30, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.income_button = ctk.CTkButton(self.sidebar_frame, text="Доход", command=self.income_button_event)
        self.income_button.grid(row=1, column=0, padx=20, pady=20)
        self.expenses_button = ctk.CTkButton(self.sidebar_frame, text="Расходы", command=self.expenses_button_event)
        self.expenses_button.grid(row=2, column=0, padx=20, pady=20)
        self.balance_button = ctk.CTkButton(self.sidebar_frame, text="Баланс", command=self.balance_button_event)
        self.balance_button.grid(row=3, column=0, padx=20, pady=20)

        # Создание полей ввода (Пользователь может вводить текст)
        self.income_frame, self.income_tree = self.create_transaction_frame("Доход", self.add_income, row=1,
                                                                            transactions=self.income_transactions)
        self.expense_frame, self.expense_tree = self.create_transaction_frame("Расход", self.add_expense, row=2,
                                                                              transactions=self.expense_transactions)
        self.balance_frame = self.create_balance_frame(row=3)

        self.hide_frames()
        self.income_frame.grid()

        self.fig = Figure(figsize=(4, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.balance_frame)
        self.canvas.get_tk_widget().grid(row=1, column=0)

    def create_transaction_frame(self, title, button_command, row, transactions):
        frame = ctk.CTkFrame(self.main_frame)
        ctk.CTkLabel(frame, text=f"Добавить {title}", font=ctk.CTkFont(size=20)).grid(row=0, column=0)

        ctk.CTkLabel(frame, text="Категория").grid(row=1, column=0)
        category_entry = ctk.CTkEntry(frame)
        category_entry.grid(row=1, column=1)

        ctk.CTkLabel(frame, text="Сумма").grid(row=2, column=0)
        amount_entry = ctk.CTkEntry(frame)
        amount_entry.grid(row=2, column=1)

        ctk.CTkButton(frame, text=f"Добавить {title}", command=lambda: button_command(category_entry, amount_entry)).grid(
            row=3, column=0)

        # Добавить таблицу транзакций
        tree = ttk.Treeview(frame)
        tree["columns"] = ("Категория", "Сумма")
        tree.column("#0", width=0, stretch="NO")
        tree.column("Категория", anchor="w", width=120)
        tree.column("Сумма", anchor="w", width=120)
        tree.heading("Категория", text="Категория", anchor='w')
        tree.heading("Сумма", text="Сумма", anchor='w')
        tree.grid(row=4, column=0, padx=20, pady=50)

        return frame, tree

    def create_balance_frame(self, row):
        frame = ctk.CTkFrame(self.main_frame)
        return frame

    # Очистка текущего представления приложения
    def hide_frames(self):
        for frame in [self.income_frame, self.expense_frame, self.balance_frame]:
            frame.grid_remove()

    def income_button_event(self):
        self.hide_frames()
        self.income_frame.grid()

    def expenses_button_event(self):
        self.hide_frames()
        self.expense_frame.grid()

    def balance_button_event(self):
        self.hide_frames()
        self.balance_frame.grid()
        self.update_plot()

    def add_income(self, category_entry, amount_entry):
        amount = self.get_amount_from_entry(amount_entry)
        category = category_entry.get()
        if amount is not None:
            self.income += amount
            self.income_transactions.append((category, amount))
            self.update_table(self.income_tree, self.income_transactions)
            category_entry.delete(0, 'end')
            amount_entry.delete(0, 'end')

    def add_expense(self, category_entry, amount_entry):
        amount = self.get_amount_from_entry(amount_entry)
        category = category_entry.get()
        if amount is not None:
            self.expense += amount
            self.expense_transactions.append((category, amount))
            self.update_table(self.expense_tree, self.expense_transactions)
            category_entry.delete(0, 'end')
            amount_entry.delete(0, 'end')

    def get_amount_from_entry(self, entry):
        try:
            amount = float(entry.get())
            if amount <= 0:
                raise ValueError
            return amount
        except ValueError:
            messagebox.showerror("Неверный ввод", "Пожалуйста, введите положительное число")
            return None

    def update_plot(self):
        self.fig.clear()
        ax = self.fig.add_subplot(111)  # Создание нового подграфика
        ax.pie([self.income, self.expense], labels=['Доход', 'Расход'], autopct='%1.1f%%')
        self.canvas.draw()

    def update_table(self, tree, transactions):
        for i in tree.get_children():
            tree.delete(i)
        for transaction in transactions:
            tree.insert('', 'end', values=transaction)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
