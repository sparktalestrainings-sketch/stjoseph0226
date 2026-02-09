import streamlit as st

# -----------------------------
# App Configuration
# -----------------------------
st.set_page_config(
    page_title="Prompt Engineering Playground",
    layout="wide"
)

st.title("🧠 Prompt Engineering Playground")
st.caption("Learn, experiment, and test prompt engineering techniques")

# -----------------------------
# Sidebar Navigation
# -----------------------------
topics = [
    "Prompt Structure & Tokens",
    "Zero-shot Prompting",
    "Few-shot Prompting",
    "Role-based Prompting",
    "Multi-turn Conversations",
    "Model Behavior Controls",
    "Flowcharts & Scenario Planning",
    "Interruptions & Error Handling",
    "Prompt Debugging"
]

selected_topic = st.sidebar.radio("📚 Select Topic", topics)

# -----------------------------
# Helper Functions
# -----------------------------
def render_prompt_inputs(show_system=True, show_examples=False):
    system_prompt = ""
    examples = ""

    if show_system:
        system_prompt = st.text_area(
            "System Prompt",
            placeholder="You are a helpful assistant..."
        )

    if show_examples:
        examples = st.text_area(
            "Examples (Few-shot)",
            placeholder="Q: ...\nA: ..."
        )

    user_prompt = st.text_area(
        "User Prompt",
        placeholder="Enter your prompt here"
    )

    return system_prompt, examples, user_prompt


def render_model_controls():
    st.subheader("⚙️ Model Controls")
    temperature = st.slider("Temperature", 0.0, 1.5, 0.7)
    max_tokens = st.slider("Max Tokens", 50, 500, 200)
    stop_seq = st.text_input("Stop Sequences (comma-separated)")

    return temperature, max_tokens, stop_seq


def mock_llm_response(prompt):
    """Mock response for local testing without API"""
    return f"[MOCK RESPONSE]\n\nProcessed Prompt:\n{prompt}"

# -----------------------------
# Topic Pages
# -----------------------------

if selected_topic == "Prompt Structure & Tokens":
    st.header("🧩 Prompt Structure & Tokens")
    st.write("Understand how prompt length and structure affect outputs.")

    system_prompt, _, user_prompt = render_prompt_inputs()

    if st.button("Run Prompt"):
        full_prompt = f"SYSTEM:\n{system_prompt}\n\nUSER:\n{user_prompt}"
        response = mock_llm_response(full_prompt)

        st.subheader("📤 Model Response")
        st.code(response)

elif selected_topic == "Zero-shot Prompting":
    st.header("🎯 Zero-shot Prompting")
    st.write("Give instructions without examples.")

    _, _, user_prompt = render_prompt_inputs(show_system=False)

    if st.button("Run Zero-shot Prompt"):
        response = mock_llm_response(user_prompt)
        st.subheader("📤 Model Response")
        st.code(response)

elif selected_topic == "Few-shot Prompting":
    st.header("📌 Few-shot Prompting")
    st.write("Guide the model with examples.")

    system_prompt, examples, user_prompt = render_prompt_inputs(show_examples=True)

    if st.button("Run Few-shot Prompt"):
        full_prompt = f"{system_prompt}\n\nEXAMPLES:\n{examples}\n\nUSER:\n{user_prompt}"
        response = mock_llm_response(full_prompt)
        st.subheader("📤 Model Response")
        st.code(response)

elif selected_topic == "Role-based Prompting":
    st.header("🎭 Role-based Prompting")
    st.write("Control behavior using system roles.")

    system_prompt = st.text_area("System Role", "You are a strict teacher")
    user_prompt = st.text_area("User Input")

    if st.button("Run Role-based Prompt"):
        full_prompt = f"SYSTEM ROLE:\n{system_prompt}\n\nUSER:\n{user_prompt}"
        response = mock_llm_response(full_prompt)
        st.subheader("📤 Model Response")
        st.code(response)

elif selected_topic == "Multi-turn Conversations":
    st.header("💬 Multi-turn Conversations")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("Your message")

    if st.button("Send") and user_input:
        st.session_state.chat_history.append(("User", user_input))
        st.session_state.chat_history.append(("Assistant", mock_llm_response(user_input)))

    for role, msg in st.session_state.chat_history:
        st.markdown(f"**{role}:** {msg}")

    if st.button("Reset Conversation"):
        st.session_state.chat_history = []

elif selected_topic == "Model Behavior Controls":
    st.header("🎛️ Controlling Model Behavior")

    user_prompt = st.text_area("User Prompt")
    temperature, max_tokens, stop_seq = render_model_controls()

    if st.button("Run with Controls"):
        debug_info = (
            f"Temp={temperature}, MaxTokens={max_tokens}, Stop={stop_seq}\n\n"
        )
        response = mock_llm_response(debug_info + user_prompt)
        st.subheader("📤 Model Response")
        st.code(response)

elif selected_topic == "Flowcharts & Scenario Planning":
    st.header("🗺️ Flowcharts & Scenario Planning")

    scenario = st.selectbox(
        "Select Scenario",
        ["Customer Support", "Interview Bot", "Tutor"]
    )

    st.markdown("**Flow:** User → Intent → Response → Follow-up")

    user_prompt = st.text_area("User Input")

    if st.button("Run Scenario"):
        response = mock_llm_response(f"Scenario: {scenario}\n{user_prompt}")
        st.subheader("📤 Model Response")
        st.code(response)

elif selected_topic == "Interruptions & Error Handling":
    st.header("⚠️ Interruptions & Error Handling")

    simulate_error = st.checkbox("Simulate API Error")
    user_prompt = st.text_area("User Input")

    if st.button("Run"):
        if simulate_error:
            st.error("Simulated API Error: Timeout")
        else:
            response = mock_llm_response(user_prompt)
            st.subheader("📤 Model Response")
            st.code(response)

elif selected_topic == "Prompt Debugging":
    st.header("🛠️ Prompt Debugging Techniques")

    original_prompt = st.text_area("Original Prompt")
    revised_prompt = st.text_area("Revised Prompt")

    if st.button("Compare"):
        st.subheader("🔍 Comparison")
        st.write("Original:")
        st.code(original_prompt)
        st.write("Revised:")
        st.code(revised_prompt)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("Built with Streamlit • Prompt Engineering Learning App")