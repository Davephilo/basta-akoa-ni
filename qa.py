import os
import csv
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
        
        self.xpath_entries = []  # Store dynamic XPath entries
        self.xpath_dropdowns = []  # Store dynamic dropdowns
        self.input_entries = []  # Store dynamic input entries
        self.input_labels = []  # Store labels for input entries
        self.sleep_entries = []  # Store sleep time entries
        self.loop_entries = []  # Store loop count entries
        self.delete_buttons = []  # Store delete buttons
        self.xpath_labels = []  # Store XPath labels
        self.sleep_labels = []  # Store sleep labels
        self.loop_labels = []  # Store loop labels
        self.equals_labels = []  # Store equals sign labels
        
        # Define uniform padding
        uniform_padx = 10
        uniform_pady = 10

        # URL Entry
        tk.Label(root, text="Enter the URL to test:").grid(row=0, column=0, padx=uniform_padx, pady=uniform_pady)
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.grid(row=0, column=1, padx=uniform_padx, pady=uniform_pady)
        
        # Test and Make EXE Button
        tk.Button(root, text="Test", command=self.submit).grid(row=0, column=2, padx=uniform_padx, pady=uniform_pady)
        tk.Button(root, text="Make EXE", command=self.make_exe).grid(row=0, column=3, padx=uniform_padx, pady=uniform_pady)

        # CSV File Selection
        tk.Label(root, text="Select your CSV file:").grid(row=1, column=0, padx=uniform_padx, pady=uniform_pady)
        self.csv_file_entry = tk.Entry(root, width=50)
        self.csv_file_entry.grid(row=1, column=1, padx=uniform_padx, pady=uniform_pady)
        tk.Button(root, text="Browse", command=self.browse_csv).grid(row=1, column=2, padx=uniform_padx, pady=uniform_pady)

        # Section for dynamic XPaths
        self.xpath_frame = tk.Frame(root)
        self.xpath_frame.grid(row=2, column=0, columnspan=10, padx=uniform_padx, pady=uniform_pady)

        # Button to add new XPath dynamically
        tk.Button(root, text="New XPath", command=self.add_xpath_row).grid(row=3, column=1, padx=uniform_padx, pady=uniform_pady)

        # Add the first XPath entry row
        self.add_xpath_row()

    def browse_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.csv_file_entry.delete(0, tk.END)
            self.csv_file_entry.insert(0, file_path)

    def add_xpath_row(self):
        row_index = len(self.xpath_entries)

        # Store widgets in a dictionary
        row_widgets = {}

        row_widgets['xpath_label'] = tk.Label(self.xpath_frame, text=f"Enter XPath {row_index + 1}:")
        row_widgets['xpath_label'].grid(row=row_index, column=0, padx=5, pady=5)
        
        row_widgets['xpath_entry'] = tk.Entry(self.xpath_frame, width=30)
        row_widgets['xpath_entry'].grid(row=row_index, column=1, padx=5, pady=5)
        
        row_widgets['equals_label'] = tk.Label(self.xpath_frame, text="=")
        row_widgets['equals_label'].grid(row=row_index, column=2, padx=5, pady=5)
        
        row_widgets['xpath_dropdown'] = ttk.Combobox(self.xpath_frame, width=15)
        row_widgets['xpath_dropdown']['values'] = ['click', 'input']
        row_widgets['xpath_dropdown'].grid(row=row_index, column=3, padx=5, pady=5)
        row_widgets['xpath_dropdown'].bind("<<ComboboxSelected>>", lambda event, idx=row_index: self.handle_dropdown_selection(idx))
        
        row_widgets['input_label'] = tk.Label(self.xpath_frame, text="Csv Header:")
        row_widgets['input_label'].grid(row=row_index, column=4, padx=5, pady=5)
        row_widgets['input_label'].grid_remove()
        
        row_widgets['input_entry'] = tk.Entry(self.xpath_frame, width=20)
        row_widgets['input_entry'].grid(row=row_index, column=5, padx=5, pady=5)
        row_widgets['input_entry'].grid_remove()
        
        row_widgets['delete_button'] = tk.Button(self.xpath_frame, text="X", command=lambda idx=row_index: self.delete_xpath_row(idx), fg="red")
        row_widgets['delete_button'].grid(row=row_index, column=10, padx=5, pady=5)
        
        self.xpath_entries.append(row_widgets)

    def delete_xpath_row(self, index):
        for widget in self.xpath_entries[index].values():
            widget.grid_remove()
        self.xpath_entries.pop(index)

    def handle_dropdown_selection(self, index):
        if self.xpath_entries[index]['xpath_dropdown'].get() == "input":
            self.xpath_entries[index]['input_label'].grid()
            self.xpath_entries[index]['input_entry'].grid()
        else:
            self.xpath_entries[index]['input_label'].grid_remove()
            self.xpath_entries[index]['input_entry'].grid_remove()

    def submit(self):
        driver = webdriver.Chrome()
        driver.maximize_window()  # Open browser in full screen
        driver.get(self.url_entry.get())
        
        for idx, row in enumerate(self.xpath_entries):
            xpath = row['xpath_entry'].get()
            action = row['xpath_dropdown'].get()
            
            if action == 'click':
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                element.click()
            elif action == 'input':
                input_value = row['input_entry'].get()
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
                element.send_keys(input_value)
        
        driver.quit()
    
    def make_exe(self):
        exe_name = simpledialog.askstring("Input", "Enter the name for the EXE file:")
        if exe_name:
            script_path = os.path.abspath(__file__)  # Get the current script's path
            os.system(f'pyinstaller --onefile --windowed -n "{exe_name}" "{script_path}"')

if __name__ == "__main__":
    root = tk.Tk()
    app = QAApp(root)
    root.mainloop()
