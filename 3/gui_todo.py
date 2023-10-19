import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

class ToDoApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ToDoリストアプリ")
        self.geometry("800x600")

        self.tasks = []

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

        # タスク完了ボタン & タスク削除ボタン
        self.complete_button = ttk.Button(self, text="タスク完了/未完了", command=self.toggle_task)
        self.complete_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = ttk.Button(self, text="タスク削除", command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=10)

    def add_task(self):
        task = self.task_entry.get()
        deadline = self.deadline_entry.get()

        if task:
            self.tasks.append((task, deadline))
            self.update_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("警告", "タスクが入力されていません")

    def toggle_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            task, deadline = self.tasks[index]
            if task.startswith("[完了] "):
                self.tasks[index] = (task[6:], deadline)
            else:
                self.tasks[index] = ("[完了] " + task, deadline)
            self.update_listbox()

    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            del self.tasks[selected_index[0]]
            self.update_listbox()

    def update_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task, deadline in self.tasks:
            # 期限が過ぎたタスクをハイライト
            if deadline < self.deadline_entry.get():
                self.task_listbox.insert(tk.END, f"{task} (期限: {deadline}) [期限超過]")
            else:
                self.task_listbox.insert(tk.END, f"{task} (期限: {deadline})")


if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()
