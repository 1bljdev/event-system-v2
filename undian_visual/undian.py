# -*- coding: utf-8 -*-
import tkinter as tk
import requests

SERVER = "http://172.16.1.13:5000"   # GANTI IP SERVER

# ================= GUI =================
root = tk.Tk()
root.attributes("-fullscreen", True)
root.configure(bg="#0b1628")

tk.Label(
    root,
    text="🏆 DOORPRIZE",
    fg="#facc15",
    bg="#0b1628",
    font=("Segoe UI", 36, "bold")
).pack(pady=30)

entry = tk.Entry(
    root,
    font=("Consolas", 42, "bold"),
    justify="center",
    width=12
)
entry.pack(pady=20)

name_label = tk.Label(
    root,
    text="",
    font=("Segoe UI", 28, "bold"),
    bg="#0b1628",
    fg="#38bdf8"
)
name_label.pack(pady=5)

division_label = tk.Label(
    root,
    text="",
    font=("Segoe UI", 20),
    bg="#0b1628",
    fg="white"
)
division_label.pack(pady=5)

status_label = tk.Label(
    root,
    text="",
    font=("Segoe UI", 16, "bold"),
    bg="#0b1628",
    fg="#facc15"
)
status_label.pack(pady=15)

step = 0  # 0 = preview, 1 = set winner

# ================= HELPER =================
def safe_post(url, payload):
    try:
        r = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException:
        return None, "❌ Server tidak dapat dihubungi"

    if r.status_code != 200:
        return None, f"❌ Server error ({r.status_code})"

    if not r.text.strip():
        return None, "❌ Respon kosong dari server"

    try:
        return r.json(), None
    except Exception:
        return None, "❌ Respon bukan JSON"

# ================= LOGIC =================
def on_enter(event):
    global step
    reg = entry.get().strip().upper()

    if not reg:
        status_label.config(text="Masukkan nomor registrasi")
        return

    # ===== PREVIEW =====
    if step == 0:
        data, err = safe_post(
            SERVER + "/preview",
            {"reg_number": reg}
        )

        if err:
            status_label.config(text=err)
            name_label.config(text="")
            division_label.config(text="")
            return

        if "error" in data:
            status_label.config(text=data["error"])
            name_label.config(text="")
            division_label.config(text="")
            return

        name_label.config(text=data.get("name", "-"))
        division_label.config(
            text=f"Divisi: {data.get('division', '-')}"
        )
        status_label.config(text="Tekan ENTER sekali lagi")
        step = 1

    # ===== SET PEMENANG =====
    else:
        data, err = safe_post(
            SERVER + "/draw_manual",
            {"reg_number": reg}
        )

        if err:
            status_label.config(text=err)
            return

        if "error" in data:
            status_label.config(text=data["error"])
            return

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
