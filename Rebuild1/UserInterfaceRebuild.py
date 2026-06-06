import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES

def create_ui(on_submit, on_file_drop):

    def submit(event=None):
        user_input = entry.get()
        entry.delete(0, tk.END)
        append_message(output, "You", user_input)
        on_submit(user_input, output)

    def filedrop(event):
        file_path = event.data
        on_file_drop(file_path)
        drop_label.config(text=f"Loaded: {file_path.strip('{}').split(chr(92))[-1]}")

    root = TkinterDnD.Tk()
    root.title("Chat")

    drop_label = tk.Label(root, text="Drop .docx or .pdf files here", relief="groove", height=3, width=60)
    drop_label.pack()
    drop_label.drop_target_register(DND_FILES)
    drop_label.dnd_bind("<<Drop>>", filedrop)

    output = tk.Text(root, height=20, width=60, state="disabled")
    output.pack()

    entry = tk.Entry(root, width=60)
    entry.pack()

    entry.bind("<Return>", submit)
    tk.Button(root, text="Send", command=submit).pack()

    root.mainloop()

def append_message(output, sender, text):
    output.config(state="normal")
    output.insert(tk.END, f"{sender}: {text}\n")
    output.config(state="disabled")
