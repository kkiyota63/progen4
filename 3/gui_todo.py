import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

class Task:
    def __init__(self, title, deadline):
        self.title = title
        self.deadline = deadline
        self.completed = False

    def toggle_completion(self):
        self.completed = not self.completed

    def is_overdue(self, current_date):
        return self.deadline < current_date

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, deadline):
        task = Task(title, deadline)
        self.tasks.append(task)

    def get_task(self, index):
        return self.tasks[index]

    def delete_task(self, index):
        del self.tasks[index]

    def toggle_task_completion(self, index):
        self.tasks[index].toggle_completion()

class ToDoApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.task_manager = TaskManager()

        self.title("ToDoリストアプリ")
        self.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        # タスク追加エントリー
        self.task_entry = ttk.Entry(self)
        self.task_entry.pack(pady=20)

        # 期限ラベル & 期限エントリー
        self.deadline_label = ttk.Label(self, text="期限:")
        self.deadline_label.pack(pady=5)
        self.deadline_entry = DateEntry(self)
        self.deadline_entry.pack(pady=5)

        # タスク追加ボタン
        self.add_button = ttk.Button(self, text="タスク追加", command=self.add_task)
        self.add_button.pack(pady=10)

        # タスク表示リストボックス
        self.task_listbox = tk.Listbox(self, height=10, width=50, selectmode=tk.SINGLE)
        self.task_listbox.pack(pady=20)

        # タスク完了ボタン
        self.complete_button = ttk.Button(self, text="タスク完了/未完了", command=self.toggle_task)
        self.complete_button.pack(side=tk.LEFT, padx=10)

        # タスク削除ボタン
        self.delete_button = ttk.Button(self, text="タスク削除", command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=10)

        # タスク編集ボタン
        self.edit_button = ttk.Button(self, text="タスク編集", command=self.edit_task)
        self.edit_button.pack(side=tk.LEFT, padx=10)

    def add_task(self):
        task_title = self.task_entry.get()
        deadline = self.deadline_entry.get()
        if task_title:
            self.task_manager.add_task(task_title, deadline)
            self.update_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("警告", "タスクが入力されていません")

    def toggle_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            self.task_manager.toggle_task_completion(selected_index[0])
            self.update_listbox()

    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            self.task_manager.delete_task(selected_index[0])
            self.update_listbox()

    def update_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.task_manager.tasks:
            task_str = "[完了] " + task.title if task.completed else task.title
            deadline_str = f"(期限: {task.deadline})"
            if task.is_overdue(self.deadline_entry.get()):
                self.task_listbox.insert(tk.END, f"{task_str} {deadline_str} [期限超過]")
            else:
                self.task_listbox.insert(tk.END, f"{task_str} {deadline_str}")

    def edit_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task = self.task_manager.get_task(selected_index[0])
            self.task_entry.delete(0, tk.END)
            self.task_entry.insert(0, task.title)
            self.deadline_entry.set_date(task.deadline)

            # タスク追加ボタンを非活性化して、編集完了ボタンを活性化
            self.add_button.config(state=tk.DISABLED)
            self.edit_button.config(text="編集完了", command=self.update_task)

    def update_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            new_task_title = self.task_entry.get()
            new_deadline = self.deadline_entry.get()
            if new_task_title:
                task = self.task_manager.get_task(selected_index[0])
                task.title = new_task_title
                task.deadline = new_deadline
                self.update_listbox()
                self.task_entry.delete(0, tk.END)

                # タスク追加ボタンを活性化して、編集完了ボタンを非活性化
                self.add_button.config(state=tk.NORMAL)
                self.edit_button.config(text="タスク編集", command=self.edit_task)
            else:
                messagebox.showwarning("警告", "タスクが入力されていません")

app = ToDoApp()
app.mainloop()
