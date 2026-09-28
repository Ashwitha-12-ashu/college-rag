import streamlit as st
import streamlit.components.v1 as components
import json

from rag import build_rag_system, ask_question


# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="College RAG Assistant",
    page_icon="🎓",
    layout="wide"
)


# -----------------------------
# TITLE
# -----------------------------

st.title("🎓 College RAG Assistant")

st.write(
    "Upload a PDF and ask questions about its content."
)


# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.header("📄 Document")

    uploaded_file = st.file_uploader(
        "Upload a PDF",
        type=["pdf"]
    )


# -----------------------------
# SESSION STATE
# -----------------------------

if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "index" not in st.session_state:
    st.session_state.index = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# PROCESS PDF
# -----------------------------

if uploaded_file is not None:

    # Process only if a new document is uploaded
    if (
        st.session_state.get("file_name")
        != uploaded_file.name
    ):

        with st.spinner("📚 Processing your PDF..."):

            pdf_path = "uploaded_document.pdf"

            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            chunks, index = build_rag_system(
                pdf_path
            )

            st.session_state.chunks = chunks
            st.session_state.index = index
            st.session_state.file_name = uploaded_file.name
            st.session_state.messages = []

        st.success(
            f"✅ {uploaded_file.name} is ready!"
        )


# -----------------------------
# DISPLAY CHAT HISTORY
# -----------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])

        # Speak previous assistant answers
        if message["role"] == "assistant":

            answer_text = json.dumps(
                message["content"]
            )

            components.html(
                f"""
                <script>

                const answer = {answer_text};

                function speakAnswer() {{

                    window.speechSynthesis.cancel();

                    const speech =
                        new SpeechSynthesisUtterance(answer);

                    speech.rate = 1.0;
                    speech.pitch = 1.0;
                    speech.volume = 1.0;

                    window.speechSynthesis.speak(speech);
                }}

                function stopAnswer() {{

                    window.speechSynthesis.cancel();

                }}

                </script>

                <button
                    onclick="speakAnswer()"
                    style="
                        padding: 8px 14px;
                        border-radius: 8px;
                        border: none;
                        cursor: pointer;
                        margin-right: 8px;
                    "
                >
                    🔊 Read Again
                </button>

                <button
                    onclick="stopAnswer()"
                    style="
                        padding: 8px 14px;
                        border-radius: 8px;
                        border: none;
                        cursor: pointer;
                    "
                >
                    ⏹ Stop
                </button>
                """,
                height=55
            )


# -----------------------------
# QUESTION INPUT
# -----------------------------

question = st.chat_input(
    "💬 Ask a question about the document..."
)


# -----------------------------
# PROCESS QUESTION
# -----------------------------

if question:

    # Check PDF
    if st.session_state.chunks is None:

        st.warning(
            "⚠️ Please upload a PDF first."
        )

    else:

        # -------------------------
        # USER MESSAGE
        # -------------------------

        with st.chat_message("user"):

            st.write(question)

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )


        # -------------------------
        # GENERATE ANSWER
        # -------------------------

        with st.chat_message("assistant"):

            with st.spinner(
                "🧠 Searching document and generating answer..."
            ):

                answer, sources = ask_question(
                    question,
                    st.session_state.chunks,
                    st.session_state.index
                )

            # Display answer
            st.write(answer)


            # -------------------------
            # TEXT TO SPEECH
            # -------------------------

            answer_text = json.dumps(answer)

            components.html(
                f"""
                <script>

                const answer = {answer_text};

                // Stop any previous speech
                window.speechSynthesis.cancel();

                // Create speech
                const speech =
                    new SpeechSynthesisUtterance(answer);

                speech.rate = 1.0;
                speech.pitch = 1.0;
                speech.volume = 1.0;

                // Try to speak automatically
                window.speechSynthesis.speak(speech);


                function speakAnswer() {{

                    window.speechSynthesis.cancel();

                    const newSpeech =
                        new SpeechSynthesisUtterance(answer);

                    newSpeech.rate = 1.0;
                    newSpeech.pitch = 1.0;
                    newSpeech.volume = 1.0;

                    window.speechSynthesis.speak(newSpeech);

                }}


                function stopAnswer() {{

                    window.speechSynthesis.cancel();

                }}

                </script>


                <div style="
                    margin-top: 10px;
                ">

                    <button
                        onclick="speakAnswer()"
                        style="
                            padding: 8px 14px;
                            border-radius: 8px;
                            border: none;
                            cursor: pointer;
                            margin-right: 8px;
                        "
                    >
                        🔊 Read Again
                    </button>

                    <button
                        onclick="stopAnswer()"
                        style="
                            padding: 8px 14px;
                            border-radius: 8px;
                            border: none;
                            cursor: pointer;
                        "
                    >
                        ⏹ Stop
                    </button>

                </div>
                """,
                height=60
            )


        # -------------------------
        # SAVE ANSWER
        # -------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )