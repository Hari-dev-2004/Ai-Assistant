import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# Load the trained model
model = load_model('chatbot_model.h5')

# Load tokenizers
with open('input_tokenizer.pkl', 'rb') as f:
    input_tokenizer = pickle.load(f)

with open('target_tokenizer.pkl', 'rb') as f:
    target_tokenizer = pickle.load(f)

# Parameters
max_input_len = 19  # Based on the model's input size
max_target_len = 19  # Based on the model's output size

model.summary()

# Function to generate a response
def generate_response(input_text):
    # Tokenize and pad input
    input_seq = input_tokenizer.texts_to_sequences([input_text])
    input_seq = pad_sequences(input_seq, maxlen=max_input_len, padding='post')

    # Predict using the model
    predictions = model.predict(input_seq)

    # Decode the predicted sequence
    decoded_sentence = ''
    for token_probs in predictions[0]:
        sampled_token_index = np.argmax(token_probs)
        sampled_word = target_tokenizer.index_word.get(sampled_token_index, '')

        if sampled_word == '\n':  # Stop if end token is found
            break

        decoded_sentence += ' ' + sampled_word

    return decoded_sentence.strip()

# Chatbot interaction loop
print("Chatbot is ready! Type 'quit' to exit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        break

    response = generate_response(user_input)
    print("Bot:", response)
