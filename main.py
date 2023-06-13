import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

openai_api_key = st.secrets["openai_api_key"]

template = """
    Below is an email that may be poorly worded.
    Your goal is to:
    - Properly format the email
    - Convert the input text to a specified tone
    - Convert the input text to a specified dialect

    Here are some examples different Tones:
    - Formal: I would appreciate further clarification on a few points in your recent proposal. Let's schedule a meeting to discuss these matters.
    - Informal: Your proposal is awesome! Got a couple of questions. Let's grab coffee or chat sometime to go over them.

    Here are some examples of words in different dialects:
    - American: Apartment, Vacation, Sidewalk, Soccer, Elevator, Cookie, Vacation, Truck, Gasoline, Pants, Cellphone, Diaper, Faucet, Fall (autumn), Mailbox
    - British: Flat, Holiday, Pavement, Football, Lift, Biscuit, Holiday, Lorry, Petrol, Trousers, Mobile, Nappy, Tap, Autumn, Postbox

    Example Sentences from each dialect:
    - American: I realized that maneuvering through the center of the parking lot was a challenge, especially when I realized that the color of my neighbor's car was spelled "gray" and not "grey" like I had grown accustomed to.
    - British: I realised that manoeuvring through the centre of the car park was a challenge, especially when I realised that the colour of my neighbour's car was spelled "grey" and not "gray" like I had grown accustomed to.

    Please start the email with a warm introduction. Add the introduction if you need to.
    
    Below is the email, tone, and dialect:
    TONE: {tone}
    DIALECT: {dialect}
    EMAIL: {email}
    
    YOUR RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["tone", "dialect", "email"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Globalize Email", page_icon=":robot:")
st.header("Email Generator")
st.markdown("_By Lloyd Koh_")
st.write("This app helps non-native English speakers communicate professionally via email. Submit your text, and our algorithms will analyze and format it for visual appeal with clear headings and paragraphs. Perfect for professionals, students, or anyone looking to improve their English writing skills.")

st.markdown("## Enter Your Email To Convert")

col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        'Which tone would you like your email to have?',
        ('Formal', 'Informal'))
    
with col2:
    option_dialect = st.selectbox(
        'Which English Dialect would you like?',
        ('American', 'British'))

def get_text():
    input_text = st.text_area(label="Email Input", label_visibility='collapsed', placeholder="Your Email...", key="email_input")
    return input_text

# Define the prompt text for the language model
prompt = "tone: {tone}\ndialect: {dialect}\nemail: {email}"

# Create a text input field for the user to enter their email
def get_text():
    input_text = st.text_area(label="Email Input", label_visibility='collapsed', placeholder="Your Email...", key="email_input")
    return input_text

email_input = get_text()

# Create a button that displays an example email when clicked
def update_text_with_example():
    st.session_state.email_input = "Kelly, I am starting work at your company on Tuesday. From, Sam."

st.button("*See An Example*", type='secondary', help="Click to see an example of the email you will be converting.", on_click=update_text_with_example)

# Create a submit button that the user can click to submit the form
submit_button = st.button("Submit")

# Define a function to process the email input
def process_email_input(email_input):
    if len(email_input.split(" ")) > 700:
        st.write("Please enter a shorter email. The maximum length is 700 words.")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_email = prompt.format(tone=option_tone, dialect=option_dialect, email=email_input)

    formatted_email = llm(prompt_with_email)

    st.write(formatted_email)

# Display the converted email if it has been processed
if "email_input" in st.session_state and submit_button and email_input:
    st.markdown("### Your Converted Email:")
    process_email_input(st.session_state.email_input)
