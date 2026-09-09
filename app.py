import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

vectorstore=FAISS.load_local('faiss_index',embeddings,allow_dangerous_deserialization=True)
retriever=vectorstore.as_retriever(search_kwargs={'k':3})

llm=ChatGoogleGenerativeAI(model='gemini-2.5-flash',google_api_key=os.getenv('GEMINI_API_KEY'))

prompt=PromptTemplate(
    input_variables=['context','question'],
    template="""
You are Atharva Pandey personal AI assistant, answering on their portfolio website.
Answer the question using ONLY the context below. Speak about Beee in third
person, in a friendly, professional tone.

If the context does not contain enough information to answer the question,
respond with exactly: NOT_FOUND

Context:
{context}

Question: {question}

Answer:

"""
)

FALLBACK_MESSAGES=(
    "I don't have that information about Atharva Pandey yet — feel free to reach out "
    "to them directly for this one!"
)

def answer_question(question:str)->str:
    #3 Retrieve relevant chunks  with similarity scores with citations
    results=vectorstore.similarity_search_with_score(question,k=10)

    if not results:
        return FALLBACK_MESSAGES,[]

    content_text="\n\n".join(doc.page_content for doc,score in results)
    final_prompt=prompt.format(context=content_text,question=question)
    response=llm.invoke(final_prompt)

    if response == "NOT_FOUND":
        return FALLBACK_MESSAGES,[]
    #3 Citations shows which chunk the answer is grounded on
    sources=[doc.page_content[:80].strip() + "..." for doc,score in results]
    return response.content,sources


## Portfolio section 
st.title('Atharva Pandey.')
st.subheader("AI/Ml Engineer in the making | Data Science")
st.write("""
Third-year B.Tech CS student building toward a career in AI/ML,
with hands-on projects across machine learning, deep learning, NLP,
and generative AI.
""")

col1,col2,col3=st.columns(3)
with col1:
    st.metric('Project Shipped','10+')
with col2:
    st.metric("12 Board %",'86.6')
with col3:
    st.metric("10 Board %",'84.6')

st.divider()
# Chatbot section #
if "messages" not in st.session_state:
    st.session_state.messages=[]

for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.write(msg['content'])
        if msg.get('sources'):
            with st.expander("Sources"):
                for s in msg['sources']:
                    st.caption(s)

user_text=st.chat_input("Ask about my skills,background,education and projects...")
if user_text:
    st.session_state.messages.append({'role':'user','content':user_text})
    with st.chat_message('user'):
        st.write(user_text)

    with st.chat_message('assistant'):
        with st.spinner('Thinking'):
            answer,sources=answer_question(user_text)
            st.write(answer)
            if sources:
                with st.expander("Sources"):
                    for s in sources:
                        st.caption(s)


    st.session_state.messages.append({'role':'assistant','content':answer,'sources':sources})




















