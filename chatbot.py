from flask import Flask, render_template, request
import nltk
from nltk.corpus import stopwords
from nltk.util import ngrams
from collections import Counter

app = Flask(__name__)

nltk.download('stopwords')

# Sample FAQ data
faq = {
    "What is your name?": "I am a chatbot.",
    "Hi": "Hi dear How can I help you?",
    "How can I contact support?": "You can contact support at support@example.com.",
    "Tell me a joke.": "Why did the computer keep freezing? Because it left its Windows open!",
    "What is your purpose?": "I'm here to assist and provide information.",
    "How does your chatbot work?": "I use natural language processing to understand your questions and provide relevant answers.",
    "Are you a human?": "No, I'm not a human. I'm an AI-powered chatbot.",
    "Can you provide technical support?": "I can offer general information, but for technical issues, please contact our support team.",
    "What are your operating hours?": "I'm available 24/7 to assist you.",
    "Where can I find more information about your services?": "You can visit our website at www.example.com for detailed information.",
    "Tell me a fun fact.": "Sure, did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
    "How can I reset my password?": "To reset your password, visit our login page and click on the 'Forgot Password' link. Follow the instructions to reset your password.",
    "What's the weather like today?": "I'm sorry, I don't have access to real-time weather information. You can check a weather website or app for the latest updates.",
    "Do you support multiple languages?": "Yes, I can understand and respond in multiple languages.",
    "What's your favorite book?": "I don't have personal preferences, but I can recommend some popular books if you'd like.",
    "Tell me a joke": "Why did the scarecrow win an award? Because he was outstanding in his field!",
}

# Dictionary to store the number of times each question has been asked
question_frequency = {question: 0 for question in faq.keys()}

# Preprocess the FAQ questions for efficient searching
faq_tokens = [nltk.word_tokenize(q.lower()) for q in faq.keys()]
stopwords_list = set(stopwords.words('english'))
faq_tokens = [[word for word in q if word.isalnum() and word not in stopwords_list] for q in faq_tokens]
faq_ngrams = [list(ngrams(q, 2)) for q in faq_tokens]
flat_ngrams = [item for sublist in faq_ngrams for item in sublist]

def get_most_similar_question(question):
    question_tokens = nltk.word_tokenize(question.lower())
    question_tokens = [word for word in question_tokens if word.isalnum() and word not in stopwords_list]
    question_ngrams = list(ngrams(question_tokens, 2))

    similarities = Counter([item for item in question_ngrams if item in flat_ngrams])
    if similarities:
        most_similar_ngram = similarities.most_common(1)[0][0]
        match_index = flat_ngrams.index(most_similar_ngram)
        return list(faq.keys())[match_index]

    return "Default Response"

def format_input_question(user_question):
    # Capitalize the first letter and convert the rest to lowercase
    return user_question.capitalize()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.form['question']
    # Format the user's input to match the FAQ question format
    formatted_question = format_input_question(user_question)
    
    # Use dict.get() to safely retrieve and update the question count
    question_frequency[formatted_question] = question_frequency.get(formatted_question, 0) + 1
    
    answer = faq.get(formatted_question, "I don't understand. Please ask another question.")  # Handle unmatched questions
    return answer


# Get the most asked question
most_asked_question = max(question_frequency, key=question_frequency.get)
most_asked_question_count = question_frequency[most_asked_question]

if __name__ == '__main__':
    app.run(debug=True)
