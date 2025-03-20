import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os

class PythonIDE(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Mini IDE")
        self.geometry("800x600")

        # Menu bar
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Run menu
        run_menu = tk.Menu(self.menu_bar, tearoff=0)
        run_menu.add_command(label="Run", command=self.run_code)
        self.menu_bar.add_cascade(label="Run", menu=run_menu)

        # Text area for code editing
        self.text_area = scrolledtext.ScrolledText(self, font=("Consolas", 12), undo=True)
        self.text_area.pack(expand=True, fill="both", padx=5, pady=5)

        # Output area
        self.output_area = scrolledtext.ScrolledText(self, height=10, font=("Consolas", 10), background="#f0f0f0")
        self.output_area.pack(fill="both", padx=5, pady=5)

        self.file_path = None

    def new_file(self):
        self.text_area.delete("1.0", tk.END)
        self.file_path = None

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", content)
            self.file_path = file_path

    def save_file(self):
        if self.file_path is None:
            self.save_file_as()
        else:
            with open(self.file_path, "w") as file:
                file.write(self.text_area.get("1.0", tk.END))

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            self.file_path = file_path
            self.save_file()

    def run_code(self):
        if self.file_path is None:
            messagebox.showerror("Error", "Please save the file before running.")
            return

        self.save_file()

        self.output_area.delete("1.0", tk.END)

        try:
            result = subprocess.run(
                ["python", self.file_path],
                capture_output=True,
                text=True,
                check=False
            )
            output = result.stdout
            error = result.stderr

            if output:
                self.output_area.insert(tk.END, output)
            if error:
                self.output_area.insert(tk.END, error)

        except Exception as e:
            self.output_area.insert(tk.END, f"Error running code:\n{e}")

if __name__ == "__main__":
    app = PythonIDE()
    app.mainloop()
