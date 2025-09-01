import streamlit as st
import google.generativeai as genai
import os



# Configure Gemini with secret
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])



# Load model
model = genai.GenerativeModel("gemini-1.5-flash")

# FAQ dictionary
FAQ = {
    "where is the library": "📚 The library is located at the Main Building, 2nd Floor, next to the IT Helpdesk.",
    "how do i register for exams": "📝 You can register for exams through the University Portal under 'Academics > Exam Registration'.",
    "what are cafeteria hours": "☕ The cafeteria is open from 8:00 AM to 8:00 PM on weekdays, and 9:00 AM to 5:00 PM on weekends.",
    "who is my academic advisor": "👨‍🏫 Your academic advisor is listed in the Student Portal under 'My Profile > Advisor Details'.",
    "how to reset my campus wifi password": "🔐 Visit the IT Helpdesk portal and select 'Forgot WiFi Password'. You will get a reset link in your student email.",
    "where can i find the class schedule": "📅 Class schedules are available in the Student Portal under 'Academics > Timetable'.",
    "how to apply for hostel accommodation": "🏠 Hostel applications can be made online through the Housing Services Portal.",
    "what sports facilities are available": "⚽ Our campus has a gym, swimming pool, basketball courts, and football field. Check the Sports Complex for details.",
    "how do i contact student services": "📞 You can email studentservices@university.edu or visit the Student Services Office at Block C, Ground Floor.",
    "where can i buy textbooks": "📖 Textbooks are available at the Campus Bookstore located beside the cafeteria. You can also order online via the bookstore portal."
}

# Function to check FAQ or fallback to Gemini
def get_response(user_input):
    cleaned = user_input.lower().strip()
    if cleaned in FAQ:
        return FAQ[cleaned]
    try:
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {e}"

# Streamlit UI
st.set_page_config(page_title="CampusBuddy", layout="centered")

# Title (smaller, one line)
# Title (one-line with emoji)
st.markdown("<h2 style='text-align: center;'>🎓 CampusBuddy - University Q&A</h2>", unsafe_allow_html=True)


# Session state for chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Input box
user_input = st.text_input("Ask me anything about campus life:")

if st.button("Ask"):
    if user_input:
        bot_response = get_response(user_input)
        st.session_state.history.append(("🧑 You", user_input))
        st.session_state.history.append(("🤖 CampusBuddy", bot_response))

# Display conversation history
for speaker, msg in st.session_state.history:
    st.markdown(f"**{speaker}:** {msg}")


