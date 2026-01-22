# -*- coding: utf-8 -*-
import tkinter as tk
import requests

SERVER = "http://172.16.2.25:5000"   # GANTI IP SERVER

root = tk.Tk()
root.attributes("-fullscreen", True)
root.configure(bg="#0b1628")

# ================= HEADER =================
tk.Label(
    root,
    text="🏆 DOORPRIZE",
    fg="#facc15",
    bg="#0b1628",
    font=("Segoe UI", 36, "bold")
).pack(pady=30)

# ================= INPUT =================
entry = tk.Entry(
    root,
    font=("Consolas", 42, "bold"),
    justify="center",
    width=12
)
entry.pack(pady=20)

# ================= NAME =================
name_label = tk.Label(
    root,
    text="",
    font=("Segoe UI", 28, "bold"),
    bg="#0b1628",
    fg="#38bdf8"
)
name_label.pack(pady=5)

# ================= DIVISION =================
division_label = tk.Label(
    root,
    text="",
    font=("Segoe UI", 20),
    bg="#0b1628",
    fg="white"
)
division_label.pack(pady=5)

# ================= STATUS =================
status_label = tk.Label(
    root,
    text="",
    font=("Segoe UI", 16, "bold"),
    bg="#0b1628",
    fg="#facc15"
)
status_label.pack(pady=15)

step = 0  # 0 = preview, 1 = set winner

# ================= LOGIC =================
def on_enter(event):
    global step
    reg = entry.get().strip().upper()

    # ===== PREVIEW =====
    if step == 0:
        r = requests.post(
            SERVER + "/preview",
            json={"reg_number": reg}
        )

        if r.status_code != 200:
            status_label.config(text=r.json().get("error", "Error"))
            name_label.config(text="")
            division_label.config(text="")
            return

        data = r.json()
        name_label.config(text=data.get("name", "-"))
        division_label.config(
            text=f"Divisi: {data.get('division', '-')}"
        )
        status_label.config(text="Tekan ENTER sekali lagi")
        step = 1

    # ===== SET PEMENANG =====
    else:
        r = requests.post(
            SERVER + "/draw_manual",
            json={"reg_number": reg}
        )

        if r.status_code != 200:
            status_label.config(text=r.json().get("error", "Error"))
            return

        data = r.json()
        name_label.config(text=data.get("name", "-"))
        division_label.config(
            text=f"Divisi: {data.get('division', '-')}"
        )
        status_label.config(text="🏆 Sudah menang 🏆")

        step = 0
        entry.delete(0, "end")

# ================= EVENTS =================
entry.bind("<Return>", on_enter)
root.bind("<Escape>", lambda e: root.destroy())

root.mainloop()
