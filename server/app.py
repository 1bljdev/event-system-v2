from flask import Flask, request, jsonify, send_file
from db import get_connection
import qrcode, io, base64, tempfile, openpyxl

app = Flask(__name__, static_url_path="/static")

# =====================================================
# INSERT GUEST
# =====================================================
def insert_guest(name, division):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO guests (name, division) VALUES (%s,%s)",
        (name, division)
    )
    conn.commit()
    return cur.lastrowid


# =====================================================
# API REGISTRASI (DESKTOP TKINTER)
# =====================================================
@app.route("/register", methods=["POST"])
def register_api():
    data = request.json
    reg_id = insert_guest(data["name"], data["division"])
    return jsonify({"reg_number": reg_id})


# =====================================================
# UI WEB REGISTRASI (MOBILE-FIRST)
# =====================================================
@app.route("/registrasi")
def registrasi():
    return """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Event Registration</title>

<style>
body {
    margin:0;
    font-family:'Segoe UI',system-ui;
    background:linear-gradient(160deg,#020617,#0f172a);
    color:white;
    min-height:100vh;
    display:flex;
    flex-direction:column;
    align-items:center;
    padding:env(safe-area-inset-top) 16px env(safe-area-inset-bottom);
}
.header {
    text-align:center;
    padding:32px 0 20px;
}
.header img {
    width:84px;
    margin-bottom:12px;
}
.header h1 {
    margin:0;
    font-size:24px;
    font-weight:700;
}
.header h2 {
    margin-top:6px;
    font-size:13px;
    font-weight:400;
    opacity:.85;
}
.card {
    width:100%;
    max-width:420px;
    background:white;
    color:#020617;
    border-radius:24px;
    padding:24px;
}
label {
    font-size:14px;
    font-weight:600;
    display:block;
    margin-top:16px;
}
input,select {
    width:100%;
    margin-top:8px;
    padding:14px;
    font-size:16px;
    border-radius:14px;
    border:1px solid #cbd5e1;
}
button {
    margin-top:24px;
    width:100%;
    padding:16px;
    font-size:16px;
    font-weight:700;
    border:none;
    border-radius:18px;
    background:#2563eb;
    color:white;
}
</style>
</head>

<body>
<div class="header">
    <img src="/static/logo.png">
    <h1>16th Operational</h1>
    <h2>PT Jakarta Lingkar Baratsatu</h2>
</div>

<div class="card">
<form method="POST" action="/register_web">
<label>Nama Lengkap</label>
<input name="name" required>

<label>Divisi</label>
<select name="division">
<option>Internal Audit & HSE</option>
<option>Management Traffic</option>
<option>Maintenance & Planning</option>
<option>Bisnis Support</option>
<option>Information Technology</option>
<option>General Affair</option>
<option>Mitra Kerja</option>
</select>

<button>DAFTAR SEKARANG</button>
</form>
</div>
</body>
</html>
"""


# =====================================================
# REGISTRASI BERHASIL + SIMPAN JPG
# =====================================================
@app.route("/register_web", methods=["POST"])
def register_web():
    reg_id = insert_guest(request.form["name"], request.form["division"])

    html = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Registrasi Berhasil</title>

<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>

<style>
body {
    margin:0;
    font-family:'Segoe UI',system-ui;
    background:linear-gradient(160deg,#020617,#0f172a);
    color:white;
    min-height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    padding:20px;
}
.card {
    width:100%;
    max-width:420px;
    background:#0b1628;
    border-radius:28px;
    padding:32px;
    text-align:center;
}
.card img {
    width:72px;
    margin-bottom:14px;
}
.reg {
    font-size:48px;
    font-weight:800;
    background:white;
    color:#020617;
    padding:20px;
    border-radius:20px;
    letter-spacing:6px;
    margin:24px 0;
}
.btn {
    width:100%;
    padding:14px;
    border-radius:14px;
    font-weight:600;
    margin-top:10px;
    border:none;
}
.save {
    background:#22c55e;
    color:white;
}
.link {
    background:transparent;
    color:#38bdf8;
}
</style>
</head>

<body>
<div class="card" id="ticket">
    <img src="/static/logo.png">
    <h2>🎉 REGISTRASI BERHASIL</h2>
    <div class="reg">REG_NUMBER</div>
    <p>Simpan nomor ini untuk undian</p>

    <button class="btn save" onclick="saveTicket()">📥 SIMPAN TIKET (JPG)</button>
    <button class="btn link" onclick="location.href='/registrasi'">➕ Daftar Lagi</button>
</div>

<script>
function saveTicket(){
 html2canvas(document.getElementById("ticket")).then(function(canvas){
   var a = document.createElement("a");
   a.href = canvas.toDataURL("image/jpeg",1.0);
   a.download = "tiket_registrasi.jpg";
   a.click();
 });
}
</script>

</body>
</html>
"""
    return html.replace("REG_NUMBER", f"{reg_id:05d}")


# =====================================================
# QR REGISTRASI
# =====================================================
@app.route("/qr_registrasi")
def qr_registrasi():
    url = request.host_url + "registrasi"
    img = qrcode.make(url)
    b = io.BytesIO()
    img.save(b, format="PNG")
    return f"<img src='data:image/png;base64,{base64.b64encode(b.getvalue()).decode()}'>"


# =====================================================
# REKAP & EXPORT
# =====================================================
@app.route("/rekap_divisi")
def rekap_divisi():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT division, COUNT(*) total
        FROM guests
        GROUP BY division
    """)
    return jsonify(cur.fetchall())


@app.route("/export_excel")
def export_excel():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Nama","Divisi","Pemenang"])

    cur.execute("SELECT name,division,is_winner FROM guests")
    for r in cur.fetchall():
        ws.append([
            r["name"],
            r["division"],
            "YA" if r["is_winner"] else "TIDAK"
        ])

    tmp = tempfile.NamedTemporaryFile(delete=False,suffix=".xlsx")
    wb.save(tmp.name)

    return send_file(tmp.name,as_attachment=True,download_name="rekap_event.xlsx")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
