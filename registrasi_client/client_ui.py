import tkinter as tk
from tkinter import ttk
import requests

SERVER = "http://172.16.2.25:5000"

root = tk.Tk()
root.title("HUT OPS Registration")
root.geometry("420x420")

tk.Label(root, text="REGISTRATION", font=("Segoe UI",16,"bold")).pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=20)

tk.Label(frame, text="Nama Lengkap").pack(anchor="w")
name = ttk.Entry(frame)
name.pack(fill="x")

tk.Label(frame, text="Divisi").pack(anchor="w", pady=(10,0))
division = ttk.Combobox(frame, state="readonly",
    values=[
        "Internal Audit & HSE",
        "Management Traffic",
        "Maintenance & Planning",
        "Bisnis Support",
        "Information Technology",
        "General Affair",
        "Mitra Kerja"
    ])
division.pack(fill="x")
division.current(0)

result = tk.Label(frame, text="")
result.pack(pady=10)

def register():
    r = requests.post(SERVER+"/register", json={
        "name": name.get(),
        "division": division.get()
    })
    result.config(text=r.json().get("reg_number","ERROR"))

tk.Button(frame, text="DAFTAR TAMU",
    bg="#2563eb", fg="white",
    command=register).pack(fill="x", pady=10)

root.mainloop()
