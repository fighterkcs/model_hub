import streamlit as st
import tempfile
from summarizer_pipeline import summarizer
from chatbot_pipeline import chat_assistant



from rag.rag_pipeline import initialize_pipeline, retrieve_and_answer


st.set_page_config(page_title="Model Studio", layout="wide")
st.title("Model Studio")


st.sidebar.title("Options")

option = st.sidebar.selectbox(
    "Select a feature",
    ["RAG", "Summarizer", "General Chatbot"]
)

if option == "RAG":
    st.header("RAG Question Answering")

    uploaded_files = st.file_uploader(
    "Upload PDF or TXT files",
    type=["pdf", "txt"],
    accept_multiple_files=True,
    key="rag_file_uploader"  
)


    query = st.text_input("Enter your question")


    if uploaded_files and "rag_ready" not in st.session_state:
        index, chunks, qa_pipe = initialize_pipeline(uploaded_files)

        st.session_state.index = index
        st.session_state.chunks = chunks
        st.session_state.qa_pipe = qa_pipe
        st.session_state.rag_ready = True

        st.success("Documents processed successfully!")

    if st.button("Get Answer"):
        if query and "rag_ready" in st.session_state:
            answer = retrieve_and_answer(
                query,
                st.session_state.index,
                st.session_state.chunks,
                st.session_state.qa_pipe
            )
            st.subheader("Answer:")
            st.write(answer)
        else:
            st.warning("Upload documents and enter a question")


elif option == "Summarizer":
    st.header("Text Summarizer")
    text= st.text_area("Enter the text which you want to summarize:")
    if st.button("Summarize"):
        if text:
            summary=summarizer(text)
            st.subheader("Summary:")
            st.markdown(summary)
        else:
            st.warning("Please enter text to summarize.")


elif option == "General Chatbot":
    st.title("Chat assistant with AGENTS")
    st.header("General Chatbot")
    input1 = st.text_area("Enter your query:")
    if st.button("Send"):
        if input1:
            response = chat_assistant(input1)
            st.subheader("Response:")
            st.markdown(response)
        else:
            st.warning("Please enter a query.")
