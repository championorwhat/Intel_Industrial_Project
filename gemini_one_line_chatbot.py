# #!/usr/bin/env python3
# """
# One-Line Gemini Chatbot - Complete Implementation
# Uses Google's new Gen AI SDK (google-genai) for reliable single-line responses
# Perfect for mood scoring and NLP analysis
# """

# import os
# import re
# import sys
# from google import genai
# from google.genai import types

# # Configuration
# GEMINI_API_KEY = "     "  # Your provided API key
# MODEL_NAME = "gemini-2.5-flash"  # Fast, reliable model for chat
# MAX_OUTPUT_TOKENS = 25  # Limit to ensure single sentence (roughly 15-20 words)
# TEMPERATURE = 0.3  # Lower temperature for more consistent, focused responses

# # System instructions to enforce single-line responses
# SYSTEM_INSTRUCTION = (
#     "You are a helpful assistant that ALWAYS responds in exactly ONE short sentence. "
#     "Never use multiple sentences, bullet points, or line breaks. "
#     "Keep responses under 20 words and end with proper punctuation."
# )

# def setup_gemini_client():
#     """Initialize the Gemini client with proper configuration"""
#     try:
#         client = genai.Client(api_key=GEMINI_API_KEY)
#         return client
#     except Exception as e:
#         print(f"Error setting up Gemini client: {e}")
#         sys.exit(1)

# def clean_response(text):
#     """Clean and ensure single-line response"""
#     if not text:
#         return "I understand."

#     # Remove any line breaks and extra whitespace
#     cleaned = re.sub(r'\s+', ' ', text.strip())

#     # Find the first complete sentence
#     sentence_match = re.search(r'^([^.!?]*[.!?])', cleaned)
#     if sentence_match:
#         return sentence_match.group(1).strip()

#     # If no punctuation found, add period and limit length
#     words = cleaned.split()
#     if len(words) > 20:
#         cleaned = ' '.join(words[:20])

#     # Ensure it ends with punctuation
#     if not cleaned.endswith(('.', '!', '?')):
#         cleaned += '.'

#     return cleaned

# def get_one_line_response(client, user_input):
#     """Generate a single-line response using Gemini"""
#     try:
#         # Enhanced prompt to ensure single-line response
#         enhanced_prompt = f"{user_input}\n\nRespond in exactly one short sentence (maximum 20 words)."

#         # Generate response with strict configuration
#         response = client.models.generate_content(
#             model=MODEL_NAME,
#             contents=[enhanced_prompt],
#             config=types.GenerateContentConfig(
#                 max_output_tokens=MAX_OUTPUT_TOKENS,
#                 temperature=TEMPERATURE,
#                 system_instruction=SYSTEM_INSTRUCTION
#             )
#         )

#         # Extract and clean the response
#         if response and response.text:
#             return clean_response(response.text)
#         else:
#             return "I understand your message."

#     except Exception as e:
#         print(f"Error generating response: {e}")
#         return "I'm having trouble understanding right now."

# def main():
#     """Main chatbot loop"""
#     print("🤖 One-Line Gemini Chatbot Ready!")
#     print("📝 Perfect for mood scoring and NLP analysis")
#     print("💬 Every response is exactly one sentence")
#     print("🔧 Type 'quit' to exit")
#     print("-" * 50)

#     # Initialize the client
#     client = setup_gemini_client()

#     # Chat loop
#     while True:
#         try:
#             # Get user input
#             user_input = input("\nYou: ").strip()

#             # Check for exit command
#             if user_input.lower() in ['quit', 'exit', 'bye']:
#                 print("Bot: Goodbye! Have a great day.")
#                 break

#             # Skip empty input
#             if not user_input:
#                 continue

#             # Generate and display response
#             bot_response = get_one_line_response(client, user_input)
#             print(f"Bot: {bot_response}")

#         except KeyboardInterrupt:
#             print("\n\nBot: Chat session ended. Goodbye!")
#             break
#         except Exception as e:
#             print(f"Unexpected error: {e}")
#             continue

# if __name__ == "__main__":
#     main()


import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")  # or "gemini-1.5-pro"

SYSTEM_PROMPT = (
    "You are an empathetic assistant. "
    "For each user message, reply with helpful, specific advice or encouragement in one short, clear sentence. "
    "Do not simply repeat the user's message."
)

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
    while True:
        user = input("You: ")
        if user.lower() == "quit":
            break
        try:
            bot = get_one_line_response(user)
            print("Bot:", bot)
        except Exception as e:
            print("Error:", e)
