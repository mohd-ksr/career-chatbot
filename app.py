import streamlit as st
from streamlit_option_menu import option_menu
from resume import resume_analyzer
from assistant import main_app

if 'intro_shown' not in st.session_state:
    st.session_state.intro_shown = False


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

def main_page():
    st.title("Career Path Oracle 🧙‍♂️")

    # Initialize session state (only once)
    if "selected_option" not in st.session_state:
        st.session_state.selected_option = "Bot Assistant"

    with st.sidebar:
        selected = option_menu(
        menu_title=None,
        options=["Bot Assistant", "Resume Analyzer"],
        icons=["robot", "gear"],
        menu_icon="cast",
        default_index=["Bot Assistant", "Resume Analyzer"].index(st.session_state.selected_option),
        orientation="horizontal",
        key="selected_option"  # <- MAGIC: direct bind to session state
        )
        st.write("---")
        st.subheader("About Me")
        st.write("I'm your Career Path Oracle and Resume Analyzer! You can ask me:")
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



    # Show content based on selection
    if st.session_state.selected_option == "Bot Assistant":
        main_app();

    elif st.session_state.selected_option == "Resume Analyzer":
        resume_analyzer();
            

# Main app entry point
if not st.session_state.intro_shown:
    show_intro()
else:
    main_page()
