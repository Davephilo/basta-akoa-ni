import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class QAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QA Tester")
        
        self.actions = []  # Store XPath, Sleep, and Scroll actions
        
        uniform_padx = 10
        uniform_pady = 10
        
        # URL Entry
        tk.Label(root, text="Enter the URL to test:").grid(row=0, column=0, padx=uniform_padx, pady=uniform_pady)
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.grid(row=0, column=1, padx=uniform_padx, pady=uniform_pady)
        
        tk.Button(root, text="Test", command=self.submit).grid(row=0, column=2, padx=uniform_padx, pady=uniform_pady)
        tk.Button(root, text="Make EXE", command=self.make_exe).grid(row=0, column=3, padx=uniform_padx, pady=uniform_pady)

        # CSV File Selection
        tk.Label(root, text="Select your CSV file:").grid(row=1, column=0, padx=uniform_padx, pady=uniform_pady)
        self.csv_file_entry = tk.Entry(root, width=50)
        self.csv_file_entry.grid(row=1, column=1, padx=uniform_padx, pady=uniform_pady)
        tk.Button(root, text="Browse", command=self.browse_csv).grid(row=1, column=2, padx=uniform_padx, pady=uniform_pady)
        
        # Scrollable Frame for Actions
        self.canvas = tk.Canvas(root, width=800, height=300)
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=2, column=0, columnspan=10, padx=uniform_padx, pady=uniform_pady, sticky='ew')
        self.scrollbar.grid(row=2, column=10, sticky='ns')

        # Buttons for Adding Actions
        button_frame = tk.Frame(root)
        button_frame.grid(row=3, column=0, columnspan=10, pady=uniform_pady)

        tk.Button(button_frame, text="New XPath", command=self.add_xpath_action).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Sleep", command=self.add_sleep_action).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Scroll", command=self.add_scroll_action).grid(row=0, column=2, padx=5)
        
        self.add_xpath_action()  # Add the first XPath action by default

    def browse_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.csv_file_entry.delete(0, tk.END)
            self.csv_file_entry.insert(0, file_path)

    def add_xpath_action(self):
        index = len(self.actions)
        action_widgets = {'type': 'xpath'}
        
        action_widgets['label_entry'] = tk.Entry(self.scrollable_frame, width=15)
        action_widgets['label_entry'].grid(row=index, column=0, padx=5, pady=5)
        
        action_widgets['xpath_entry'] = tk.Entry(self.scrollable_frame, width=30)
        action_widgets['xpath_entry'].grid(row=index, column=1, padx=5, pady=5)
        
        action_widgets['equals_label'] = tk.Label(self.scrollable_frame, text="=")
        action_widgets['equals_label'].grid(row=index, column=2, padx=5, pady=5)
        
        action_widgets['action_dropdown'] = ttk.Combobox(self.scrollable_frame, width=15)
        action_widgets['action_dropdown']['values'] = ['click', 'input']
        action_widgets['action_dropdown'].grid(row=index, column=3, padx=5, pady=5)
        action_widgets['action_dropdown'].bind("<<ComboboxSelected>>", lambda event, idx=index: self.handle_dropdown_selection(idx))
        
        action_widgets['input_label'] = tk.Label(self.scrollable_frame, text="CSV Header:")
        action_widgets['input_label'].grid(row=index, column=4, padx=5, pady=5)
        action_widgets['input_label'].grid_remove()
        
        action_widgets['input_entry'] = tk.Entry(self.scrollable_frame, width=20)
        action_widgets['input_entry'].grid(row=index, column=5, padx=5, pady=5)
        action_widgets['input_entry'].grid_remove()
        
        action_widgets['delete_button'] = tk.Button(self.scrollable_frame, text="X", command=lambda idx=index: self.delete_action(idx), fg="red")
        action_widgets['delete_button'].grid(row=index, column=6, padx=5, pady=5)
        
        self.actions.append(action_widgets)

    def add_sleep_action(self):
        index = len(self.actions)
        action_widgets = {'type': 'sleep'}
        
        action_widgets['label'] = tk.Label(self.scrollable_frame, text="Sleep (sec):")
        action_widgets['label'].grid(row=index, column=0, padx=5, pady=5)
        
        action_widgets['sleep_entry'] = tk.Entry(self.scrollable_frame, width=10)
        action_widgets['sleep_entry'].grid(row=index, column=1, padx=5, pady=5)
        
        action_widgets['delete_button'] = tk.Button(self.scrollable_frame, text="X", command=lambda idx=index: self.delete_action(idx), fg="red")
        action_widgets['delete_button'].grid(row=index, column=2, padx=5, pady=5)
        
        self.actions.append(action_widgets)

    def add_scroll_action(self):
        index = len(self.actions)
        action_widgets = {'type': 'scroll'}
        
        action_widgets['label'] = tk.Label(self.scrollable_frame, text="Scroll (px):")
        action_widgets['label'].grid(row=index, column=0, padx=5, pady=5)
        
        action_widgets['scroll_entry'] = tk.Entry(self.scrollable_frame, width=10)
        action_widgets['scroll_entry'].grid(row=index, column=1, padx=5, pady=5)
        
        action_widgets['delete_button'] = tk.Button(self.scrollable_frame, text="X", command=lambda idx=index: self.delete_action(idx), fg="red")
        action_widgets['delete_button'].grid(row=index, column=2, padx=5, pady=5)
        
        self.actions.append(action_widgets)

    def delete_action(self, index):
        action = self.actions.pop(index)
        for key, widget in action.items():
            if isinstance(widget, tk.Widget):
                widget.grid_remove()
                widget.destroy()
        
        # Refresh action indices
        for i, action in enumerate(self.actions):
            if 'delete_button' in action:
                action['delete_button'].config(command=lambda idx=i: self.delete_action(idx))

    def handle_dropdown_selection(self, index):
        if self.actions[index]['action_dropdown'].get() == "input":
            self.actions[index]['input_label'].grid()
            self.actions[index]['input_entry'].grid()
        else:
            self.actions[index]['input_label'].grid_remove()
            self.actions[index]['input_entry'].grid_remove()

    def submit(self):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(self.url_entry.get())

        for action in self.actions:
            pass  # Implement action execution here

        driver.quit()
    
    def make_exe(self):
        exe_name = simpledialog.askstring("Input", "Enter the name for the EXE file:")
        if exe_name:
            script_path = os.path.abspath(__file__)
            os.system(f'pyinstaller --onefile --windowed -n "{exe_name}" "{script_path}"')

if __name__ == "__main__":
    root = tk.Tk()
    app = QAApp(root)
    root.mainloop()
