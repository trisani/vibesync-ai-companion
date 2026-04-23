import base64
import numpy as np
import cv2
import re
from deepface import DeepFace
from flask import Flask, render_template, request, jsonify
import ollama

app = Flask(__name__)

current_emotion = "neutral"

# -------------------- CLEAN REPLY FUNCTION --------------------
def clean_reply(text):
    text = re.sub(r'Instruction.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'##.*', '', text)
    return text.strip()

# -------------------- HOME --------------------
@app.route("/")
def home():
    return render_template("index.html")

# -------------------- EMOTION DETECTION (FAST) --------------------
@app.route("/detect_emotion", methods=["POST"])
def detect_emotion():
    global current_emotion

    data = request.json["image"]
    image_data = base64.b64decode(data.split(",")[1])
    np_arr = np.frombuffer(image_data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    try:
        result = DeepFace.analyze(
            frame,
            actions=['emotion'],
            enforce_detection=False,
            detector_backend='opencv'  # 🔥 faster
        )
        current_emotion = result[0]['dominant_emotion']
    except:
        current_emotion = "neutral"

    return jsonify({"emotion": current_emotion})

# -------------------- CHAT --------------------
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    # 🔥 CLEAN + NATURAL PROMPT (NO INSTRUCTION LEAK)
    system_prompt = (
        f"The user currently seems {current_emotion}. "
        "Respond in a warm, natural, human-like way. "
        "Be supportive and emotionally aware. "
        "Keep the reply short and conversational. "
        "Do NOT include any instructions, labels, or meta text."
    )

    try:
        response = ollama.chat(
            model="phi3",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response["message"]["content"]
        reply = clean_reply(reply)  # 🔥 remove unwanted text

        return jsonify({
            "reply": reply,
            "emotion": current_emotion
        })

    except Exception as e:
        return jsonify({
            "reply": "⚠️ Something went wrong. Please try again.",
            "emotion": current_emotion
        })

# -------------------- RUN --------------------
if __name__ == "__main__":
    app.run(debug=True)