from flask import Flask, request, jsonify, send_from_directory
import ollama

app = Flask(__name__, static_folder=".")


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()

    vraag = data.get("message", "").strip()

    if not vraag:
        return jsonify({
            "answer": "Ik heb geen bericht ontvangen."
        })

    try:

        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Je bent O.R.I.O.N., "
                        "een futuristische AI-assistent. "
                        "Antwoord in het Nederlands wanneer "
                        "de gebruiker Nederlands spreekt. "
                        "Wees vriendelijk, slim en natuurlijk."
                    )
                },
                {
                    "role": "user",
                    "content": vraag
                }
            ]
        )

        antwoord = response["message"]["content"]

        return jsonify({
            "answer": antwoord
        })

    except Exception as fout:

        return jsonify({
            "answer": "AI ERROR: " + str(fout)
        })


if __name__ == "__main__":

    print("O.R.I.O.N. SERVER ONLINE")
    print("Open: http://127.0.0.1:5000")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )