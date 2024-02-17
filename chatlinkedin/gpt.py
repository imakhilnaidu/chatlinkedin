from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI


def main():
    load_dotenv()

    # Extracting text from file
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = " ".join([page.extract_text() for page in pdf_reader.pages])

        # Splitting into chunks
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=0,
            length_function=len
        )

        chunks = text_splitter.split_text(text)

        # create embeddings
        embeddings = OpenAIEmbeddings()
        knowledge_base = FAISS.from_texts(chunks, embeddings)

        if user_question:
            docs = knowledge_base.similarity_search(user_question)

            llm = OpenAI(temperature=0)
            chain = load_qa_chain(llm, chain_type="stuff")
            response = chain.run(input_documents=docs, question=user_question)



if __name__ == '__main__':
    main()