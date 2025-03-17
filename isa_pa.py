import tkinter as tk
from tkinter import filedialog, ttk
import csv

class CSVReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Reader")
        
        self.load_button = tk.Button(root, text="Load CSV", command=self.load_csv)
        self.load_button.pack(pady=10)

        self.header_combobox = ttk.Combobox(root, state="readonly")
        self.header_combobox.pack(pady=10)

        self.select_button = tk.Button(root, text="Select Header", command=self.display_selected_header)
        self.select_button.pack(pady=10)

        self.text_widget = tk.Text(root, wrap='word', width=80, height=20)
        self.text_widget.pack(pady=10)

        self.rows = []  # To store the CSV data
        self.headers = []  # To store the headers

    def load_csv(self):
        # Open a file dialog to select a CSV file
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, mode='r') as file:
                csv_reader = csv.DictReader(file)
                self.rows = list(csv_reader)
                self.headers = self.rows[0].keys() if self.rows else []
                self.header_combobox['values'] = list(self.headers)  # Populate the combobox with headers

    def display_selected_header(self):
        selected_header = self.header_combobox.get()
        if selected_header and self.rows:
            self.text_widget.delete(1.0, tk.END)  # Clear the text widget
            self.text_widget.insert(tk.END, f"Values for '{selected_header}':\n")
            self.text_widget.insert(tk.END, "-" * (len(f"Values for '{selected_header}':") + 2) + "\n")  # Separator line
            
            # Display the values for the selected header
            for row in self.rows:
                value = row[selected_header]
                self.text_widget.insert(tk.END, f"{value}\n")

# Create the main window
root = tk.Tk()
app = CSVReaderApp(root)

# Start the Tkinter event loop
root.mainloop()