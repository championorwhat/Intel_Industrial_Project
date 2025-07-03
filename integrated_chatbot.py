import os
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")  # or "gemini-1.5-pro"

SYSTEM_PROMPT = (
    "You are an empathetic assistant. "
    "For each user message, reply with helpful, specific advice or encouragement in one short, clear sentence. "
    "Do not simply repeat the user's message."
)

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn.functional import softmax
import torch

# Load model
model_name = "bhadresh-savani/distilbert-base-uncased-emotion"
tokenizer = AutoTokenizer.from_pretrained(model_name)
emotion_model = AutoModelForSequenceClassification.from_pretrained(model_name)

# 5-mood mapping
def predict_emotion_and_score(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = emotion_model(**inputs)
    probs = softmax(outputs.logits, dim=1)
    pred_id = torch.argmax(probs).item()
    label = emotion_model.config.id2label[pred_id].lower()

    if label in ["joy", "love", "amusement", "admiration", "approval", "caring", "optimism", "pride", "relief"]:
        mood = "Happy"
        score = 90
    elif label in ["realization", "neutral", "curiosity"]:
        mood = "Calm"
        score = 70
    elif label in ["confusion", "nervousness", "surprise"]:
        mood = "Confused"
        score = 50
    elif label in ["sadness", "disappointment", "grief", "remorse", "embarrassment"]:
        mood = "Sad"
        score = 30
    elif label in ["anger", "disgust", "fear", "disapproval"]:
        mood = "Angry"
        score = 15
    else:
        mood = "Calm"
        score = 60

    return mood, score

def get_one_line_response(user_input):
    prompt = (
        f"{SYSTEM_PROMPT}\n"
        f"User: {user_input}\n"
        "Assistant (one sentence):"
    )
    response = model.generate_content(prompt)
    # Take only the first sentence, remove line breaks
    text = response.text.strip().replace('\n', ' ')
    # Optionally, limit to the first sentence:
    import re
    match = re.search(r"([^.?!]+[.?!])", text)
    return match.group(1).strip() if match else text

if __name__ == "__main__":
    print("🤖 One-Line Gemini Chatbot Ready!")
    print("📝 Perfect for mood scoring and NLP analysis")
    print("💬 Every response is exactly one sentence")
    print("🔧 Type 'quit' to exit")
    print("-" * 50)

    user_inputs = []  # To collect chat messages

    while True:
        user = input("You: ")
        if user.lower() == "quit":
            break
        user_inputs.append(user)
        try:
            bot = get_one_line_response(user)
            print("Bot:", bot)
        except Exception as e:
            print("Error:", e)
            try:
                bot = get_one_line_response(user)
                print("Bot:", bot)
            except Exception as e:
                print("Error:", e)

    # ✅ This runs AFTER the chat ends
    print("\n📊 Analyzing your chat mood...")

    scores = []
    moods = []

    for text in user_inputs:
        mood, score = predict_emotion_and_score(text)
        scores.append(score)
        moods.append(mood)

    if scores:
        avg_score = sum(scores) / len(scores)
        dominant_mood = max(set(moods), key=moods.count)

        print(f"\n✅ Final Mood Score: {round(avg_score, 2)}")
        print(f"🎭 Overall Mood: {dominant_mood}")
    else:
        print("No user inputs to analyze.")
