import streamlit as st
import google.generativeai as genai
import os 

# 🔹 Configure Gemini AI
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 🔹 FAQ database with keywords
faq_data = {
    "library": {
        "keywords": ["library", "books", "study area"],
        "answer": "📚 The library is located at the Main Campus, open 8AM – 10PM daily."
    },
    "exam": {
        "keywords": ["exam", "register", "paper", "examination"],
        "answer": "📝 You can register for exams via the student portal under the 'Examinations' tab."
    },
    "canteen": {
        "keywords": ["canteen", "food", "cafeteria", "lunch", "dining"],
        "answer": "🍽️ The university canteen is near Block A, open from 7AM – 9PM."
    },
    "sports": {
        "keywords": ["sports", "gym", "football", "basketball", "badminton"],
        "answer": "⚽ Sports facilities include a gym, football field, and courts. Students can book via the sports office."
    },
    "wifi": {
        "keywords": ["wifi", "internet", "connection", "network"],
        "answer": "📶 Connect to the WiFi 'UniNet' with your student ID and portal password."
    },
    "admission": {
        "keywords": ["admission", "apply", "enroll", "registration"],
        "answer": "🎓 Admission applications can be submitted online via the official university portal."
    },
    "hostel": {
        "keywords": ["hostel", "dorm", "accommodation", "room"],
        "answer": "🏠 Hostel applications are handled by the Housing Office. Apply early as rooms are limited."
    },
    "transport": {
        "keywords": ["bus", "transport", "shuttle", "parking"],
        "answer": "🚌 Shuttle buses run every 30 minutes between the hostel and campus. Parking permits can be applied via the portal."
    },
    "fees": {
        "keywords": ["fees", "tuition", "payment", "bill"],
        "answer": "💰 Tuition fees can be paid through the finance portal or at the university finance office."
    },
    "graduation": {
        "keywords": ["graduation", "convocation", "ceremony"],
        "answer": "🎉 Graduation ceremonies are held twice a year. Eligible students will be notified via email."
    }
}

# 🔹 Match keywords with user input
def get_faq_answer(user_input: str):
    user_input = user_input.lower()
    for faq, data in faq_data.items():
        for keyword in data["keywords"]:
            if keyword in user_input:
                return data["answer"]
    return None  # No match found

# 🔹 Main chatbot function
def chatbot_response(user_input):
    # 1. Try FAQ keywords
    faq_answer = get_faq_answer(user_input)
    if faq_answer:
        return faq_answer
    
    # 2. If no match, fallback to Gemini AI
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        return f"⚠️ Error with AI: {e}"

# 🔹 Streamlit UI
st.set_page_config(page_title="CampusBuddy", page_icon="🎓")

st.markdown("<h3 style='text-align: center;'>🎓 CampusBuddy - University Q&A</h3>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if user_input := st.chat_input("Ask me anything about the university..."):
    # Save & display user message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate bot response
    response = chatbot_response(user_input)
    st.session_state["messages"].append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
