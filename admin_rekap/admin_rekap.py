import tkinter as tk
from tkinter import ttk, messagebox
import requests
import webbrowser

SERVER = "http://172.16.2.25:5000"  # ganti jika pakai ngrok

root = tk.Tk()
root.geometry("500x400")
root.title("Rekap Peserta")

tree = ttk.Treeview(root, columns=("d","t"), show="headings")
tree.heading("d", text="Divisi")
tree.heading("t", text="Jumlah")
tree.pack(fill="both", expand=True, padx=10, pady=10)

def load():
    tree.delete(*tree.get_children())
    try:
        r = requests.get(SERVER + "/rekap_divisi", timeout=5)

        if r.status_code != 200:
            raise Exception("Server error")

        data = r.json()

        for row in data:
            tree.insert("", "end", values=(
                row.get("division", "-"),
                row.get("total", 0)
            ))

    except Exception:
        messagebox.showerror(
            "Error",
            "Gagal mengambil data dari server.\n\n"
            "Pastikan:\n"
            "- Server Flask hidup\n"
            "- URL SERVER benar\n"
            "- Endpoint /rekap_divisi ada"
        )

tk.Button(root, text="🔄 Refresh", command=load).pack(pady=5)

tk.Button(
    root,
    text="📤 Export Excel",
    command=lambda: webbrowser.open(SERVER + "/export_excel")
).pack(pady=5)

load()
root.mainloop()
