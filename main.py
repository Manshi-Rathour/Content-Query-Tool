import os
import streamlit as st
import time
from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from dotenv import load_dotenv
load_dotenv()

st.title("Article Research Tool 📈")
st.sidebar.title("Article URLs")

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    if url:
        urls.append(url)

process_url_clicked = st.sidebar.button("Process URL(s)")
faiss_index_path = "faiss_index_openai"

main_placeholder = st.empty()
llm = OpenAI(temperature=0.9, max_tokens=500)

# Initialize session state
if "urls_processed" not in st.session_state:
    st.session_state.urls_processed = False

if process_url_clicked:
    try:
        # load data
        loader = UnstructuredURLLoader(urls=urls)
        main_placeholder.text("Data Loading...Started...✅✅✅")
        data = loader.load()
        # split data
        text_splitter = RecursiveCharacterTextSplitter(
            separators=['\n\n', '\n', '.', ','],
            chunk_size=1000
        )
        main_placeholder.text("Text Splitter...Started...✅✅✅")
        docs = text_splitter.split_documents(data)
        # create embeddings and save it to FAISS index
        embeddings = OpenAIEmbeddings()
        vectorstore_openai = FAISS.from_documents(docs, embeddings)
        main_placeholder.text("Embedding Vector Started Building...✅✅✅")
        time.sleep(2)

        # Save the FAISS index to a local file
        vectorstore_openai.save_local(faiss_index_path)

        # Update session state
        st.session_state.urls_processed = True

    except Exception as e:
        st.error(f"An error occurred while processing URLs: {e}")
        print("Exception occurred while processing URLs:", e)

query = main_placeholder.text_input("Question: ")
if query:
    if st.session_state.urls_processed:
        embeddings = OpenAIEmbeddings()  # Redefine embeddings here
        if os.path.exists(faiss_index_path):
            try:
                vectorstore = FAISS.load_local(faiss_index_path, embeddings, allow_dangerous_deserialization=True)
                chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())
                result = chain({"question": query}, return_only_outputs=True)
                print("Result: ", result)
                # result will be a dictionary of this format --> {"answer": "", "sources": [] }
                st.header("Answer")
                st.write(result["answer"])

                # Display sources, if available
                sources = result.get("sources", "")
                if sources:
                    st.subheader("Sources:")
                    sources_list = sources.split("\n")  # Split the sources by newline
                    for source in sources_list:
                        st.write(source)

            except Exception as e:
                st.error(f"An error occurred while retrieving the answer: {e}")
                print("Exception occurred while retrieving the answer:", e)

        else:
            st.error("Please process the URLs first.")
            print("FAISS index file not found. Please process the URLs first.")

    else:
        st.error("Please process the URLs first.")
        print("URLs not processed. Please process the URLs first.")

else:
    if not st.session_state.urls_processed:
        st.info("Please enter URL(s) and click 'Process URL(s)' to proceed.")
        print("No query provided and URLs not processed.")
    else:
        st.info("Please enter a question to get an answer.")
        print("No query provided.")
