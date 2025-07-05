# import streamlit as st
# import textwrap
# import time
# from utils.transcript import get_transcript
# from utils.explain import explain_text_eli5
# from utils.summary import generate_timestamped_summaries, generate_full_summary
# from utils.quiz import generate_quiz_from_text
# from utils.rag_qa import generate_rag_answer
# from utils.smart_chunking import smart_chunk_text

# st.set_page_config(page_title="Smart Video Study Assistant", layout="wide")
# st.title("Smart Video Study Assistant")

# # Sidebar: Info and Settings
# with st.sidebar:
#     st.header("Settings")
#     model_options = [
#         "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
#         "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
#         "mistralai/Mixtral-8x7B-Instruct-v0.1"
#     ]
#     selected_models = st.multiselect("Model fallback order", model_options, default=model_options[:2])
#     st.markdown("---")
#     st.info("Choose your preferred models here. The app will try them in order if one fails.")

# # Video Input
# st.markdown("Paste a YouTube video link to get started:")
# video_url = st.text_input("Enter YouTube video URL")

# if st.button("Get Transcript") and video_url:
#     with st.spinner("⏳ Fetching transcript..."):
#         transcript, error = get_transcript(video_url)

#     if error:
#         st.error(f"Error fetching transcript: {error}")
#     elif transcript:
#         st.session_state.transcript = transcript
#         st.success("Transcript fetched successfully!")

#         st.subheader("🔍 Transcript Preview (first 5 lines)")
#         for entry in transcript[:5]:
#             st.markdown(f"**{entry['start']:.2f}s → {entry['start'] + entry['duration']:.2f}s**: {entry['text']}")

# # After Transcript Load
# if "transcript" in st.session_state:
#     transcript = st.session_state.transcript
#     full_transcript = " ".join([entry["text"] for entry in transcript])

#     st.markdown("### Full Transcript")
#     st.text_area("Transcript", full_transcript, height=400)
#     st.download_button("Download Transcript", full_transcript, file_name="transcript.txt", mime="text/plain")

#     def play_audio(text):
#         import pyttsx3
#         engine = pyttsx3.init()
#         engine.save_to_file(text, 'summary_audio.mp3')
#         engine.runAndWait()
#         with open('summary_audio.mp3', 'rb') as audio_file:
#             audio_bytes = audio_file.read()
#         return audio_bytes

#     # Audio for Transcript
#     if st.button("🔊 Play Transcript Audio"):
#         audio_bytes = play_audio(full_transcript)
#         st.audio(audio_bytes, format='audio/mp3')

#     # ---------------- ELI5 Explanation ----------------
#     st.markdown("### Explain Like I'm 5 (ELI5)")
#     explanation_mode = st.radio("Choose explanation style:", ["Chunked", "Full context"])

#     if st.button("Generate ELI5 Explanation"):
#         with st.spinner("Generating explanation..."):
#             explanations = []
#             model_used = None

#             if explanation_mode == "Chunked":
#                 chunks = textwrap.wrap(full_transcript, width=1000)
#                 for i, chunk in enumerate(chunks):
#                     explanation, model_used = explain_text_eli5(chunk, model_priority=selected_models)
#                     explanations.append(f"### Part {i+1}\n{explanation}\n")
#             else:
#                 explanation, model_used = explain_text_eli5(full_transcript, max_tokens=2048, model_priority=selected_models)
#                 explanations = [explanation]

#             full_explanation = "\n\n".join(explanations)
#             st.subheader("📘 ELI5 Explanation")
#             st.success(full_explanation)
#             st.download_button("⬇️ Download Explanation", full_explanation, file_name="explanation.txt", mime="text/plain")

#             # Audio for ELI5 Explanation
#             if st.button("Play ELI5 Explanation Audio"):
#                 audio_bytes = play_audio(st.session_state.eli5_explanation)
#                 st.audio(audio_bytes, format='audio/mp3')

#     # ---------------- Summary Generator ----------------
#     st.markdown("### Summary Generator")
#     summary_style = st.radio("Choose summary style:", ["Timestamped Chunked", "Full context"], key="summary_style")

#     if st.button("Generate Summary"):
#         with st.spinner("Summarizing transcript..."):
#             if summary_style == "Timestamped Chunked":
#                 summaries = generate_timestamped_summaries(transcript)
#                 for segment in summaries:
#                     st.markdown(f"**{segment['start']:.2f}s → {segment['end']:.2f}s**")
#                     st.success(segment["summary"])
#             else:
#                 summary, model_used = generate_full_summary(transcript, model_priority=selected_models)
#                 st.success(summary)
#                 st.caption(f"Model used: {model_used}")
#                 st.download_button("⬇️ Download Summary", summary, file_name="summary.txt", mime="text/plain")

#                 # Audio for Summary
#                 if st.button("🔊 Play Summary Audio"):
#                     audio_bytes = play_audio(summary)
#                     st.audio(audio_bytes, format='audio/mp3')

#     # ---------------- Quiz Generator ----------------
#     st.markdown("### Quiz Generator")
#     quiz_chunking = st.checkbox("Enable Smart Chunking for quiz generation", value=True)

#     if st.button("Generate Quiz"):
#         with st.spinner("Generating quiz questions..."):
#             try:
#                 start_time = time.time()
#                 quiz_output = generate_quiz_from_text(full_transcript, chunking_enabled=quiz_chunking, model_priority=selected_models)
#                 all_questions_text = "\n\n".join(q["questions"] for q in quiz_output)
#                 st.code(all_questions_text)
#                 used_models = list(set(q["model"] for q in quiz_output if q["model"]))
#                 st.caption(f"Models used: {', '.join(used_models)}")
#                 st.download_button("Download Quiz", all_questions_text, file_name="quiz.txt", mime="text/plain")
#                 st.success(f"Quiz generated in {time.time() - start_time:.2f} seconds")
#             except Exception as e:
#                 st.error(f"Failed to generate quiz: {e}")

#     # ---------------- RAG-based Q&A ----------------
#     st.markdown("### Ask Questions (RAG-based Q&A)")
#     user_question = st.text_input("Ask your question about the video:")

#     if st.button("🔍 Get Answer") and user_question:
#         with st.spinner("Retrieving answer from transcript..."):
#             try:
#                 answer, top_chunks = generate_rag_answer(
#                     question=user_question,
#                     transcript_chunks=transcript,
#                     model_priority=selected_models,
#                     k=4
#                 )
#                 st.subheader("Answer")
#                 st.success(answer)
#                 st.markdown("### Supporting Snippets:")
#                 for chunk in top_chunks:
#                     start = chunk['start']
#                     end = chunk['start'] + chunk['duration']
#                     st.markdown(f"**{start:.2f}s → {end:.2f}s**")
#                     st.info(chunk['text'])
#             except Exception as e:
#                 st.error(f"Failed to retrieve answer: {e}")

# # ---------------- PDF Export and Voice Reading Features ----------------
# st.markdown("---")

# # PDF Export
# if "full_summary" in st.session_state:
#     from fpdf import FPDF
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     pdf.multi_cell(0, 10, st.session_state.full_summary)
#     pdf_output = pdf.output(dest='S').encode('latin1')
#     st.download_button("Download Summary as PDF", pdf_output, file_name="summary.pdf", mime="application/pdf")

# # Voice Reading (Text-to-Speech)
# import pyttsx3

# def play_audio(text):
#     engine = pyttsx3.init()
#     engine.save_to_file(text, 'summary_audio.mp3')
#     engine.runAndWait()
#     with open('summary_audio.mp3', 'rb') as audio_file:
#         audio_bytes = audio_file.read()
#     return audio_bytes

# # Show audio player after generating ELI5 explanation
# if "eli5_explanation" in st.session_state:
#     st.markdown("### 🔊 Listen to ELI5 Explanation")
#     if st.button("Play ELI5 Explanation Audio"):
#         audio_bytes = play_audio(st.session_state.eli5_explanation)
#         st.audio(audio_bytes, format='audio/mp3')

# # Show audio player after generating full summary
# if "full_summary" in st.session_state:
#     st.markdown("### 🔊 Listen to Summary")
#     if st.button("Play Summary Audio"):
#         audio_bytes = play_audio(st.session_state.full_summary)
#         st.audio(audio_bytes, format='audio/mp3')

# # Show audio player after generating full transcript (optional)
# if "transcript" in st.session_state:
#     full_transcript = " ".join([entry["text"] for entry in st.session_state.transcript])
#     st.markdown("### 🔊 Listen to Full Transcript")
#     if st.button("Play Full Transcript Audio"):
#         audio_bytes = play_audio(full_transcript)
#         st.audio(audio_bytes, format='audio/mp3')



import streamlit as st
import textwrap
import time
from utils.transcript import get_transcript
from utils.explain import explain_text_eli5
from utils.summary import generate_timestamped_summaries, generate_full_summary
from utils.quiz import generate_quiz_from_text
from utils.rag_qa import generate_rag_answer
from utils.smart_chunking import smart_chunk_text

st.set_page_config(page_title="Smart Video Study Assistant", layout="wide")
st.title("Smart Video Study Assistant")

# Sidebar: Info and Settings
with st.sidebar:
    st.header("Settings")
    model_options = [
        "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
        "mistralai/Mixtral-8x7B-Instruct-v0.1"
    ]
    selected_models = st.multiselect("Model fallback order", model_options, default=model_options[:2])
    st.markdown("---")
    st.info("Choose your preferred models here. The app will try them in order if one fails.")

# Video Input
st.markdown("Paste a YouTube video link to get started:")
video_url = st.text_input("Enter YouTube video URL")

if st.button("Get Transcript") and video_url:
    with st.spinner("Fetching transcript..."):
        transcript, error = get_transcript(video_url)

    if error:
        st.error(f"Error fetching transcript: {error}")
    elif transcript:
        st.session_state.transcript = transcript
        st.success("Transcript fetched successfully!")

        st.subheader("Transcript Preview (first 5 lines)")
        for entry in transcript[:5]:
            st.markdown(f"**{entry['start']:.2f}s → {entry['start'] + entry['duration']:.2f}s**: {entry['text']}")

# After Transcript Load
if "transcript" in st.session_state:
    transcript = st.session_state.transcript
    full_transcript = " ".join([entry["text"] for entry in transcript])

    st.markdown("### Full Transcript")
    st.text_area("Transcript", full_transcript, height=400)
    st.download_button("Download Transcript", full_transcript, file_name="transcript.txt", mime="text/plain")

    # ---------------- ELI5 Explanation ----------------
    st.markdown("### Explain Like I'm 5 (ELI5)")
    explanation_mode = st.radio("Choose explanation style:", ["Chunked", "Full context"])

    if st.button("Generate ELI5 Explanation"):
        with st.spinner("Generating explanation..."):
            explanations = []
            model_used = None

            if explanation_mode == "Chunked":
                chunks = textwrap.wrap(full_transcript, width=1000)
                for i, chunk in enumerate(chunks):
                    explanation, model_used = explain_text_eli5(chunk, model_priority=selected_models)
                    explanations.append(f"### Part {i+1}\n{explanation}\n")
            else:
                explanation, model_used = explain_text_eli5(full_transcript, max_tokens=2048, model_priority=selected_models)
                explanations = [explanation]

            full_explanation = "\n\n".join(explanations)
            st.subheader("ELI5 Explanation")
            st.success(full_explanation)
            st.download_button("Download Explanation", full_explanation, file_name="explanation.txt", mime="text/plain")

    # ---------------- Summary Generator ----------------
    st.markdown("### Summary Generator")
    summary_style = st.radio("Choose summary style:", ["Timestamped Chunked", "Full context"], key="summary_style")

    if st.button("Generate Summary"):
        with st.spinner("Summarizing transcript..."):
            if summary_style == "Timestamped Chunked":
                summaries = generate_timestamped_summaries(transcript)
                for segment in summaries:
                    st.markdown(f"**{segment['start']:.2f}s → {segment['end']:.2f}s**")
                    st.success(segment["summary"])
            else:
                summary, model_used = generate_full_summary(transcript, model_priority=selected_models)
                st.success(summary)
                st.caption(f"Model used: {model_used}")
                st.download_button("Download Summary", summary, file_name="summary.txt", mime="text/plain")

    # ---------------- Quiz Generator ----------------
    st.markdown("### Quiz Generator")
    quiz_chunking = st.checkbox("Enable Smart Chunking for quiz generation", value=True)

    if st.button("Generate Quiz"):
        with st.spinner("Generating quiz questions..."):
            try:
                start_time = time.time()
                quiz_output = generate_quiz_from_text(full_transcript, chunking_enabled=quiz_chunking, model_priority=selected_models)
                all_questions_text = "\n\n".join(q["questions"] for q in quiz_output)
                st.code(all_questions_text)
                used_models = list(set(q["model"] for q in quiz_output if q["model"]))
                st.caption(f"Models used: {', '.join(used_models)}")
                st.download_button("Download Quiz", all_questions_text, file_name="quiz.txt", mime="text/plain")
                st.success(f"Quiz generated in {time.time() - start_time:.2f} seconds")
            except Exception as e:
                st.error(f"Failed to generate quiz: {e}")

    # ---------------- RAG-based Q&A ----------------
    st.markdown("### Ask Questions (RAG-based Q&A)")
    user_question = st.text_input("Ask your question about the video:")

    if st.button("Get Answer") and user_question:
        with st.spinner("Retrieving answer from transcript..."):
            try:
                answer, top_chunks = generate_rag_answer(
                    question=user_question,
                    transcript_chunks=transcript,
                    model_priority=selected_models,
                    k=4
                )
                st.subheader("Answer")
                st.success(answer)
                st.markdown("### Supporting Snippets:")
                for chunk in top_chunks:
                    start = chunk['start']
                    end = chunk['start'] + chunk['duration']
                    st.markdown(f"**{start:.2f}s → {end:.2f}s**")
                    st.info(chunk['text'])
            except Exception as e:
                st.error(f"Failed to retrieve answer: {e}")
