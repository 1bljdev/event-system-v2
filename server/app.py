from flask import Flask, request, jsonify
from db import get_connection

app = Flask(__name__)

# =====================================================
# PREVIEW PESERTA (STEP 1)
# =====================================================
@app.route("/preview", methods=["POST"])
def preview():
    data = request.json
    reg = int(data["reg_number"])

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM guests WHERE id=%s", (reg,))
    g = cur.fetchone()

    if not g:
        return jsonify({"error": "Nomor tidak terdaftar"})

    if g["is_winner"]:
        return jsonify({"error": "Peserta sudah pernah menang"})

    return jsonify({
        "name": g["name"],
        "division": g["division"]
    })


# =====================================================
# SET PEMENANG (STEP 2)
# =====================================================
@app.route("/draw_manual", methods=["POST"])
def draw_manual():
    data = request.json
    reg = int(data["reg_number"])

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM guests WHERE id=%s", (reg,))
    g = cur.fetchone()

    if not g:
        return jsonify({"error": "Nomor tidak terdaftar"})

    if g["is_winner"]:
        return jsonify({"error": "Peserta sudah pernah menang"})

    cur.execute(
        "UPDATE guests SET is_winner=1 WHERE id=%s",
        (reg,)
    )
    conn.commit()

    return jsonify({
        "name": g["name"],
        "division": g["division"]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
