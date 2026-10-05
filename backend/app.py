from models import llm,model
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate

#   Loading the database:
store = Chroma(
    persist_directory="vectorStore",
    embedding_function=model
)

#   Retriever:
retriever = store.as_retriever()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


#   Chat Loop:
history=[]
while True :
    question=input('Human: ')

    if question.strip().lower() in ["exit", "bye"]:
        break


    history.append(f'HumanMessage:{question}')
    
    prompt = ChatPromptTemplate.from_template('''
    You are a Helpful assistant. 
    Answer the user's questions using the information provided in the retrieved context from the Harry Potter book.

    Rules:

    * Use only the provided context to answer.
    * Do not make up information.
    * If the answer is not present in the context, say: "I don't know based on the provided book."
    * Give clear and concise answers.
    * Do not mention the retrieval process unless asked.

    Context:
    {context}

    Question:
    {question}

    history:
    {history}
    '''
    )

    chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough(),
        "history": lambda _: history
    }
    | prompt
    | llm
)


    response = chain.invoke(question)   
    print(response.content)
    history.append(f'AI_Message:{response.content}')