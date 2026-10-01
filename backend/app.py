from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
load_dotenv()


#   Models:
llm=ChatGroq(
    model='openai/gpt-oss-20b'
)

model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


#   Loading the database:
store = Chroma(
    persist_directory="vectorStore",
    embedding_function=model
)

#   Retriever:
retriever = store.as_retriever()


#   Chat Loop:
while True :
    question=input('Human: ')

    if question.strip().lower() in ["exit", "bye"]:
        break

    docs=retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs)
    
    prompt=f'''
    You are a Helpful assistant. 
    Answer the user's questions using the information provided in the retrieved context from the Harry Potter book.

    Rules:

    * Use only the provided context to answer.
    * Do not make up information.
    * If the answer is not present in the context, say: "I don't know based on the provided book."
    * Give clear and concise answers.
    * Do not mention the retrieval process unless asked.

    question: {question},
    context: {context}
    '''

    response=llm.invoke(prompt)
    print(response.content)