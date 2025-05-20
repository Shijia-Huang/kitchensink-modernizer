import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
try:
    from analyze_code import analyze_code, insert_suffix
except ImportError:
    raise ImportError("Could not import analyze_code. Please make sure analyze_code.py exists and is in the same directory.")

def select_input_file():
    path = filedialog.askopenfilename(filetypes=[("Java Files", "*.java")])
    if path:
        input_path_var.set(path)

def run_analysis(mode):
    input_path = input_path_var.get()
    output_path = output_path_var.get().strip()

    if not input_path:
        messagebox.showerror("Error", "Input file path is required.")
        return

    if not output_path:
        output_path = insert_suffix(input_path, f"_{mode}")

    log_output.insert(tk.END, f"Running in '{mode}' mode...\n")
    log_output.insert(tk.END, f"Input: {input_path}\n")
    log_output.insert(tk.END, f"Output: {output_path}\n")
    log_output.insert(tk.END, "Please wait...\n")
    log_output.update()

    try:
        analyze_code(input_path, output_path, mode)
        log_output.insert(tk.END, "Done!\n\n")
    except Exception as e:
        log_output.insert(tk.END, f"Error: {e}\n\n")

#
# Set up GUI with drag-and-drop support
root = TkinterDnD.Tk()
root.title("Java Code Annotator")

tk.Label(root, text="Input File Path:").grid(row=0, column=0, sticky="w")
input_path_var = tk.StringVar()
# Drop-enabled entry for input file path
input_entry = tk.Entry(root, textvariable=input_path_var, width=60)
input_entry.grid(row=0, column=1, padx=5)
input_entry.drop_target_register(DND_FILES)
input_entry.dnd_bind('<<Drop>>', lambda e: input_path_var.set(e.data.strip('{}')))
tk.Button(root, text="Browse", command=select_input_file).grid(row=0, column=2)

tk.Label(root, text="Output File Path (optional):").grid(row=1, column=0, sticky="w")
output_path_var = tk.StringVar()
tk.Entry(root, textvariable=output_path_var, width=60).grid(row=1, column=1, padx=5)

tk.Button(root, text="Comment", width=15, command=lambda: run_analysis("comment")).grid(row=2, column=1, sticky="w", pady=10)
tk.Button(root, text="Modernize", width=15, command=lambda: run_analysis("modernize")).grid(row=2, column=1, sticky="e", pady=10)

log_output = scrolledtext.ScrolledText(root, width=90, height=20)
log_output.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()