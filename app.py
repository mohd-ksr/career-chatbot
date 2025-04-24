import streamlit as st
import google.generativeai as genai
import graphviz
import os
from dotenv import load_dotenv
import time
import re
import PyPDF2
import docx
# Load environment variables
load_dotenv()
# Initialize session state for page control
if 'intro_shown' not in st.session_state:
    st.session_state.intro_shown = False


def render_enhanced_flowchart(steps):
        dot = graphviz.Digraph(format='png', engine='dot')

        # Loop through the steps and assign rectangular shapes and fill colors
        for idx, step in enumerate(steps):
            dot.node(f"step{idx}", step, shape='rectangle', style='filled', fillcolor="#4e5a75", fontcolor="white", width="2")

            # Create edges between nodes if it's not the first node
            if idx > 0:
                dot.edge(f"step{idx-1}", f"step{idx}")

        # Render the flowchart in Streamlit
        st.graphviz_chart(dot)


def show_intro():
    # Introduction page code (unchanged)
    st.markdown("""
    <style>
    @media (max-width: 768px) {
        .intro-container { padding: 1rem; }
        .feature-icon { font-size: 2rem; }
        .intro-title { font-size: 2rem; }
        .intro-subtitle { font-size: 1.25rem; }
        .team-member { margin-bottom: 1rem; }
    }
    .intro-container {
        padding: 2rem;
        background-color: #f0f2f6;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    .feature-icon:hover {
        transform: scale(1.1);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="intro-container">
        <div style="text-align: center;">
            <img src="https://cdn-icons-png.flaticon.com/512/10349/10349936.png" 
                 style="max-width: 150px; height: auto; margin: 0 auto;"/>
        </div>
        <h1 style="color: #4A90E2; font-size: 2.5rem;">Career Path Oracle 🧙‍♂️</h1>
        <h3 style="color: #333; margin-top: 0.5rem;">Your AI-Powered Career Companion</h3>
        <p style="text-align: center; color: #555;">
            Get personalized career guidance, skill analysis, and job market insights
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("---")

    # Features row
    st.subheader("What I Can Do For You")
    feature_cols = st.columns(3)
    features = [
        ("📝", "Resume Analysis", "Extract skills and get tailored career suggestions"),
        ("🕵️", "Job Market Insights", "Discover relevant job postings and salary data"),
        ("📚", "Learning Resources", "Get free course recommendations to upskill")
    ]
    
    for idx, (icon, title, desc) in enumerate(features):
        with feature_cols[idx]:
            st.markdown(f"""
            <div style="text-align: center; margin: 1.5rem 0;">
                <span class="feature-icon">{icon}</span>
                <h4>{title}</h4>
                <p style="color: #666; font-size: 0.9rem;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.write("---")
    
    # Team row
    st.subheader("Our Team")
    team_cols = st.columns(3)
    team = [
        ("Pavan", "12305446", "ML Engineer"),
        ("Sakshi", "12306499", "Data Scientist"),
        ("Kausar", "12316343", "ML Engineer")
    ]
    
    for idx, (name, id, role) in enumerate(team):
        with team_cols[idx]:
            st.markdown(f"""
            <div style="text-align: center; margin: 1rem 0;">
                <h4>{name}</h4>
                <p style="color: #666; font-size: 0.85rem;">
                    {role}<br>
                    <code style="background: #f0f2f6;">ID: {id}</code>
                </p>
            </div>
            """, unsafe_allow_html=True)

    st.write("---")
    
    # How it works
    st.subheader("How It Works")
    steps = ["1. Upload/Describe Skills", "2. Get Career Suggestions", 
             "3. Explore Opportunities", "4. Refine Search"]
    step_cols = st.columns(4)
    for idx, step in enumerate(steps):
        with step_cols[idx]:
            st.markdown(f"""
            <div style="text-align: center;">
                <h2 style="color: #4A90E2;">{idx+1}</h2>
                <p>{step}</p>
            </div>
            """, unsafe_allow_html=True)

    if st.button("Let's Get Started ➡️", use_container_width=True):
        st.session_state.intro_shown = True
        st.rerun()

def main_app():
        
    # Configure Gemini API
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your-gemini-api-key")
    genai.configure(api_key=GEMINI_API_KEY)

    # Define generation config
    generation_config = genai.types.GenerationConfig(
        temperature=0.7,
        top_p=0.9,
        max_output_tokens=5000,
    )

    with st.sidebar:
        st.write("---")
        st.subheader("About Me")
        st.write("I'm your Career Path Oracle! You can ask me:")
        st.write("- About myself and how I can help you")
        st.write("- For career path suggestions")
        st.write("- About job market insights")
        st.write("- For learning resources")
        
        st.write("---")
        st.subheader("Example Questions")
        st.write("Try asking:")
        st.write("- What skills do I need for data science?")
        st.write("- What are the best career paths for Python developers?")
        st.write("- How can I transition to AI engineering?")
        st.write("- Make 1 year roadmap for becoming MERN developer")
        
        st.write("---")
        st.subheader("Team Members")
        st.write("Pavan - 12305446")
        st.write("Sakshi - 12306499")
        st.write("Kausar - 12316343")


    # Title
    st.title("Career Path Oracle 🧙‍♂️")

    with st.expander("📄 Upload your resume for instant career suggestions and pathways",expanded=False):     
        uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
        def extract_skills(resume_text):
            
            prompt = f"""
            You are a career assistant. From the following resume content, extract all the relevant professional skills.
            Include programming languages, tools, technologies, frameworks, cloud services, and soft skills.
            Return the result as a clean comma-separated list with no extra commentary.

            Resume:
            \"\"\"
            {resume_text}
            \"\"\"
            """

            try:
                # response = model.generate_content(prompt)
                response = genai.GenerativeModel("gemini-2.0-flash").generate_content(prompt)
                # Clean and split the response into a list
                raw_output = response.text.strip()
                skills = [skill.strip() for skill in raw_output.split(",") if skill.strip()]
                return skills
            except Exception as e:
                print("Error during Gemini skill extraction:", e)
                return []


        # Function to read PDF file
        def read_pdf(file):
            with open(file, "rb") as f:
                pdf_reader = PyPDF2.PdfReader(f)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return text

        # Function to read DOCX file
        def read_docx(file):
            doc = docx.Document(file)
            text = ""
            for para in doc.paragraphs:
                text += para.text
            return text

        # Function to get career paths based on skills using Gemini
        def get_career_paths(skills):
            # Prompt Gemini with the extracted skills to generate a career path
            prompt = f" Act like you are reading skills from a resume of a person and Given the skills: {', '.join(skills)}, suggest some relevant career paths. And also suggest high paying job roles in each pathways"
            response = genai.GenerativeModel("gemini-2.0-flash").generate_content(prompt)
            return response.text

        # Streamlit UI for file upload
        st.markdown("Resume Analyzer for Career Pathways")

        # Check and process only once
        if uploaded_file and "resume_processed" not in st.session_state:
            if uploaded_file.type == "application/pdf":
                resume_text = read_pdf(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                resume_text = read_docx(uploaded_file)
            else:
                resume_text = ""

            skills = extract_skills(resume_text)
            if skills:
                career_paths = get_career_paths(skills)

            # Save in session state
            st.session_state.resume_text = resume_text
            st.session_state.skills = skills
            st.session_state.career_paths = career_paths
            st.session_state.resume_processed = True

            if "resume_processed" in st.session_state:
                skills = st.session_state.skills
                career_paths = st.session_state.career_paths

            
                if skills:
                    st.write(f"Mentioned Skills in resume: {', '.join(skills)}")               
                    # Get career suggestions based on the skills
                    # career_paths = get_career_paths(skills)
                    placeholder = st.empty()
                    displayed_text = ""
                    # Word-by-word streaming
                    blocks = re.split(r"(?<=\n)\n+", career_paths.strip())
                    for block in blocks:
                        block = block.strip()
                        words = block.split(" ")
                        for word in words:
                            displayed_text += word + " "
                            placeholder.markdown(displayed_text + "▌", unsafe_allow_html=True)
                            time.sleep(0.01)
                        displayed_text += "\n\n"
                        placeholder.markdown(displayed_text + "▌", unsafe_allow_html=True)
                        time.sleep(0.1)   
                    placeholder.markdown(displayed_text, unsafe_allow_html=True)
                else:
                    st.write("No skills were identified in your resume.")
            # Optional reset button
            if st.button("🔁 Reset Resume Upload"):
                for key in ["resume_text", "skills", "career_paths", "resume_processed"]:
                    st.session_state.pop(key, None)
                st.rerun()






    # Semantic check function using Gemini
    def is_career_related_semantically(query):
        classifier_model = genai.GenerativeModel("gemini-2.0-flash")
        classification_prompt = f"""
        You are an expert classifier. Your task is to analyze the user input below and determine whether it is asking for career guidance, planning, job preparation, learning roadmap, or role-specific advice.

        A valid input may include things like:
        - Planning a career in a specific field (e.g., "I want to become a data analyst. Help me plan.")
        - Creating a roadmap or study plan to become something (e.g., "How to become a machine learning engineer?")
        - Job search or resume advice
        - Skills, courses, or certifications for a role
        - Interview preparation, industry expectations, or portfolio suggestions

        An invalid input is anything unrelated to careers, such as:
        - Creative writing, storytelling, history, politics, general facts, entertainment, or casual conversation.

        Now, evaluate the input below:

        "{query}"

        Is this clearly a career-related request? Answer only with 'Yes' or 'No'.
        """

        result = classifier_model.generate_content(classification_prompt)
        return result.text.strip().lower().startswith("yes")


    # Session state
    if "chat" not in st.session_state:
        model = genai.GenerativeModel("gemini-2.0-flash", generation_config=generation_config)
        st.session_state.chat = model.start_chat(history=[])
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            if msg.get("type") == "flowchart": render_enhanced_flowchart(msg["data"]) 
            else:st.markdown(msg["text"], unsafe_allow_html=True)


    # Function to use Gemini to generate job roles dynamically
    def get_job_roles_from_gemini(field):
        prompt = f"Given the field of {field}, suggest a list of relevant job roles in this domain."

        # Request Gemini to generate relevant job roles
        response = st.session_state.chat.send_message(prompt)
        roles = response.text.strip()

        if not roles:
            roles = "Career roles could not be determined. Please specify the field of interest."

        return roles



    # Function to generate career roadmap using Gemini
    def get_career_steps_from_gemini(career_field):
        prompt = f"Generate a career roadmap for someone wanting to become a {career_field}. List 10 to 15 steps in chronological order. Keep the list clear and concise.Simply generate list nothing else means not any starting text or highlighting text"
        
        # Request Gemini to generate career steps
        response = genai.GenerativeModel("gemini-2.0-flash").generate_content(prompt)
        
        steps = response.text.strip().split("\n")
        return steps


    # User input
    prompt = st.chat_input("Ask anything about your career path...")

    

    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "text": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                if is_career_related_semantically(prompt):
                    # Analyze the query to extract a field (using Gemini's assistance)
                    field_identification_prompt = (
                        f"Based on the user's query, determine the field they are referring to. "
                        f"User query: \"{prompt}\". Provide only the carrer and job field, like 'Machine Learning', 'Data Science',Web development,AI, Cloud Computing, etc."
                    )

                    field_response = st.session_state.chat.send_message(field_identification_prompt)
                    field_of_interest = field_response.text.strip()
                    modified_prompt=""
                    steps=[]
                    if field_of_interest:
                        # Get job roles dynamically based on the field of interest
                        job_roles = get_job_roles_from_gemini(field_of_interest)
                        # Append the job roles suggestion to the prompt
                        modified_prompt = (
                        f"{prompt}\n\n"
                        f"**And Relevant Job Roles in {field_of_interest}:**\n{job_roles}\n\n"
                        f"**And suggest some online courses on various plateform such as on udemy and coursera on the topic of {field_of_interest} with examples coureses name"
                        )
                        steps = get_career_steps_from_gemini(field_of_interest)


                    response = st.session_state.chat.send_message(modified_prompt)
                    full_text = response.text+"\n\nFlow Chart"


                    placeholder = st.empty()
                    displayed_text = ""

                    # Word-by-word streaming
                    blocks = re.split(r"(?<=\n)\n+", full_text.strip())
                    for block in blocks:
                        block = block.strip()
                        words = block.split(" ")
                        for word in words:
                            displayed_text += word + " "
                            placeholder.markdown(displayed_text + "▌", unsafe_allow_html=True)
                            time.sleep(0.01)
                        displayed_text += "\n\n"
                        placeholder.markdown(displayed_text + "▌", unsafe_allow_html=True)
                        time.sleep(0.1)

                    # Final output
                    placeholder.markdown(displayed_text, unsafe_allow_html=True)
                    st.session_state.chat_history.append({"role": "assistant", "text": full_text})

                    # Flowchart
                    if len(steps)>0:
                        render_enhanced_flowchart(steps)

                    st.session_state.chat_history.append({ "role": "assistant", "type": "flowchart", "data": steps })
                else:
                    default_msg = (
                    "I'm here to assist you with career guidance, job preparation, learning roadmaps, "
                    "and planning for your professional journey. If you have questions about how to enter "
                    "a specific field, what skills to develop, or how to grow in your role — I’d be glad to help!\n\n"
                    "However, this particular request doesn't seem related to career development, so I won’t be able to assist with it. "
                    "Please feel free to ask me anything related to your career path."
                    )
                    st.markdown(default_msg)
                    st.session_state.chat_history.append({"role": "assistant", "text": default_msg})


# Main app entry point
if not st.session_state.intro_shown:
    show_intro()
else:
    main_app()


