import streamlit as st
from streamlit_mic_recorder import speech_to_text

def record_voice(language="en"):
    state = st.session_state

    if "text_received" not in state:
        state.text_received = []

    text = speech_to_text(
        start_prompt="Click and speak to ask a question",
        stop_prompt="Stop recording ",
        language=language,
        use_container_width=True,
        just_once=True,
    )

    if text:
        state.text_received.append(text)

    result = "".join(state.text_received)
    state.text_received = []

    return result if result else None
