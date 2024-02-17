from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import openai

import os

openai.api_key = "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"
training_data = []
csv_folder_path = "assets/LinkedInData"
for file_name in os.listdir(csv_folder_path):
    if file_name.endswith(".csv"):
        with open(os.path.join(csv_folder_path, file_name), "rb") as file:
            # Attempt to decode with different encodings
            encodings = ["utf-8", "ISO-8859-1", "utf-16"]
            for encoding in encodings:
                try:
                    lines = file.read().decode(encoding).splitlines()
                    for line in lines:
                        training_data.append(line.strip())
                    break  # Break out of the loop if successful
                except UnicodeDecodeError:
                    continue

# Combine text from all CSV files
text = "\n".join(training_data)

text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=0, separator=" ")
chunks = text_splitter.split_text(text)
embeddings = HuggingFaceEmbeddings()
print("embeddings started ....")
docs = FAISS.from_texts(chunks, embeddings)
print("embeddings finished ....")


def ask_question(question):
    text = docs.similarity_search(question, k=1)[0]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[
        {"role": "user", "content": f"'{text}' please answer this question, {question}?"}])
    return response["choices"][0]["message"]["content"]


print(ask_question("what is your name?"))
