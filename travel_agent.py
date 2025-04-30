import streamlit as st
from praisonaiagents import Agent, Agents, MCP
from dotenv import load_dotenv
import os
import io
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from prompt import prompt
# Add for PDF and image export
from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont
import tempfile


# Load environment variables
load_dotenv()

# --- Authentication Page ---
def authentication_page():
    st.set_page_config(page_title="Travel LLM Agent", layout="wide")
    st.title("🔒 Travel LLM Agent Login")
    st.markdown("Choose your login method:")
    
    login_method = st.radio(
        "Login Method",
        ["Use Password", "Enter API Keys Directly"]
    )
    
    if login_method == "Use Password":
        password = st.text_input("Password", type="password")
        submit = st.button("Submit Password", type="primary")
        if submit:
            if password == os.getenv("PASSWORD"):
                # Use default keys from .env
                default_groq = os.getenv("GROQ_API_KEY", "")
                default_brave = os.getenv("BRAVE_API_KEY", "")
                if not default_groq or not default_brave:
                    st.error("Default API keys not found in .env. Please contact admin or use direct API key entry.")
                    st.stop()
                st.session_state["GROQ_API_KEY"] = default_groq
                st.session_state["BRAVE_API_KEY"] = default_brave
                st.session_state["authenticated"] = True
                st.experimental_rerun()
            else:
                st.error("Incorrect password. Please try again or use direct API key entry.")
    
    else:  # Enter API Keys Directly
        st.markdown("Enter your API keys:")
        groq_api_key = st.text_input("GROQ_API_KEY", type="password", key="groq_api_key_input")
        brave_api_key = st.text_input("BRAVE_API_KEY", type="password", key="brave_api_key_input")
        submit_keys = st.button("Submit API Keys", key="submit_keys_btn", type="primary")
        if submit_keys:
            if not groq_api_key or not brave_api_key:
                st.error("Both API keys are required.")
                st.stop()
            st.session_state["GROQ_API_KEY"] = groq_api_key
            st.session_state["BRAVE_API_KEY"] = brave_api_key
            st.session_state["authenticated"] = True
            st.experimental_rerun()

# --- Main App Page ---
def main_page():
    st.set_page_config(page_title="Travel LLM Agent", layout="wide")
    def get_api_keys():
        groq_api_key = st.session_state.get("GROQ_API_KEY", "")
        brave_api_key = st.session_state.get("BRAVE_API_KEY", "")
        if not groq_api_key or not brave_api_key:
            st.sidebar.error("API keys missing. Please restart and login again.")
            st.stop()
        os.environ["GROQ_API_KEY"] = groq_api_key
        os.environ["BRAVE_API_KEY"] = brave_api_key
        return groq_api_key, brave_api_key

    groq_api_key, brave_api_key = get_api_keys()

    # --- File Parsing Function ---
    def parse_uploaded_file(uploaded_file):
        try:
            file_bytes = uploaded_file.read()
            file_name = uploaded_file.name
            file_extension = os.path.splitext(file_name)[1].lower()
            file_like_object = io.BytesIO(file_bytes)
            temp_file_path = f"./temp_{file_name}"
            with open(temp_file_path, "wb") as f:
                f.write(file_bytes)
            content = ""
            if file_extension == ".csv":
                df = pd.read_csv(temp_file_path)
                content = df.to_markdown(index=False)
            elif file_extension == ".pdf":
                loader = PyPDFLoader(file_path=temp_file_path)
                documents = loader.load()
                content = "\n".join([doc.page_content for doc in documents])
            elif file_extension == ".txt":
                loader = TextLoader(file_path=temp_file_path, encoding='utf-8')
                documents = loader.load()
                content = "\n".join([doc.page_content for doc in documents])
            else:
                st.warning(f"Unsupported file type: {file_extension}. Please upload CSV, PDF, or TXT.")
                content = "None (Unsupported file type)"
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            return content
        except Exception as e:
            st.error(f"Error parsing file {uploaded_file.name}: {e}")
            if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            return "None (Error parsing file)"

    # --- Agent Definitions ---
    def create_agents(api_key, include_flight_agent=True, include_hotel_agent=True):
        mcp_tool = MCP("npx -y @modelcontextprotocol/server-brave-search", env={"BRAVE_API_KEY": api_key})
        llm_model = "groq/deepseek-r1-distill-llama-70b"
        agents_list = []
        research_agent = Agent(
            instructions="Research travel destinations, attractions, local customs, travel requirements, and seasonal events. Gather detailed information about unique experiences, cultural significance, weather patterns, local transportation options, safety considerations, and visa requirements. Identify off-the-beaten-path attractions that align with user preferences while avoiding overcrowded tourist spots. Research local etiquette, tipping customs, and cultural sensitivities to enhance the traveler's experience.",
            llm=llm_model,
            tools=mcp_tool
        )
        agents_list.append(research_agent)
        if include_flight_agent:
            flight_agent = Agent(
                instructions="Search for available flights, compare prices, and recommend optimal flight choices within the specified budget. Provide detailed information including airlines, flight numbers, departure/arrival times, layovers, baggage allowances, and total costs. Prioritize flights with the best balance of price, convenience, and comfort. Suggest alternative dates or nearby airports if they offer significant cost savings. Include booking platform recommendations and highlight any special offers or loyalty programs.",
                llm=llm_model,
                tools=mcp_tool
            )
            agents_list.append(flight_agent)
        if include_hotel_agent:
            hotel_agent = Agent(
            instructions="Research hotels and accommodation options that precisely match the user's budget and stated preferences. Provide comprehensive details including hotel name, star rating, location convenience, room types, amenities (pool, spa, free breakfast, etc.), and approximate costs per night. Consider proximity to planned activities and transportation options. Include booking details, cancellation policies, and special offers. For luxury preferences, focus on high-end amenities and exceptional service; for budget constraints, prioritize value and essential comforts.",
            llm=llm_model,
                tools=mcp_tool
            )
            agents_list.append(hotel_agent)
        planning_agent = Agent(
            instructions="Design detailed day-by-day travel plans incorporating activities, transportation, dining, and adequate rest time. Create balanced itineraries with realistic timing that account for travel between locations. Avoid overscheduling and allow flexibility. For each day, include specific time blocks for activities, estimated travel times between locations, recommended restaurants with cuisine types and price ranges, and approximate costs for all components. Ensure the total daily and trip costs stay within budget. Suggest backup activities for weather contingencies and include local transportation recommendations. If existing plans are provided, identify inefficiencies and suggest improvements while preserving core elements.",
            llm=llm_model,
            tools=mcp_tool
        )
        agents_list.append(planning_agent)
        return Agents(agents=agents_list)

    # --- Streamlit UI ---
    st.title("🌍 Travel Planning Assistant")
    st.markdown("Plan your next trip with the help of AI agents!")
    with st.sidebar:
        st.header("Trip Details")
        destination = st.text_input("Destination(s)", "Udaipur and Mount Abu")
        dates = st.text_input("Travel Dates", "May 2 to May 6 2025")
        budget = st.text_input("Budget", "Total RS. 50000")
        preferences = st.text_area("Preferences", "Historical sites, local cuisine, luxury stay, avoiding crowded tourist traps")
        include_flights = st.checkbox("Include Flight Search?", value=True)
        include_hotels = st.checkbox("Include Hotel Recommendations?", value=True)
        st.markdown("**Existing Plans (Optional)**")
        uploaded_file = st.file_uploader("Upload existing plan (CSV, PDF, TXT)", type=["csv", "pdf", "txt"])
        existing_plans_text = st.text_area("Or enter existing plans here:", "None")
        generate_plan = st.button("Generate Travel Plan", type="primary")
    if generate_plan:
        if not destination or not dates or not budget or not preferences:
            st.warning("Please fill in all the trip details.")
        else:
            st.info("🤖 Agents are working on your travel plan...")
            try:
                existing_plans_content = "None"
                if uploaded_file is not None:
                    st.info(f"Processing uploaded file: {uploaded_file.name}...")
                    with st.spinner('Parsing file...'):
                        existing_plans_content = parse_uploaded_file(uploaded_file)
                    st.success(f"File {uploaded_file.name} processed.")
                elif existing_plans_text and existing_plans_text.lower() != 'none':
                    existing_plans_content = existing_plans_text
                travel_query = f"""Plan a trip to {destination} from {dates}.\nBudget: {budget}\nPreferences: {preferences}\nExisting Plans-\n{existing_plans_content}\n\nGenerate a detailed day-by-day itinerary including {'potential flights, ' if include_flights else ''}{'accommodation options (fitting the budget and preferences), ' if include_hotels else ''}attractions to visit (focusing on preferences and avoiding crowds), and local customs or tips.\n"""
                with st.expander("View Generated Prompt"):
                    st.code(travel_query, language='text')
                travel_query += prompt
                travel_agents = create_agents(brave_api_key, include_flight_agent=include_flights, include_hotel_agent=include_hotels)
                with st.spinner('Generating plan... This might take a moment.'):
                    result = travel_agents.start(travel_query)
                st.success("Travel plan generated!")
                st.markdown("""
                    <style>
                    .scrollable-result {
                        max-height: 500px;
                        overflow-y: auto;
                        padding: 1em;
                        border: 1px solid #e0e0e0;
                        background: #fafafa;
                        margin-bottom: 1em;
                    }
                    </style>
                """, unsafe_allow_html=True)
                st.markdown('<div class="scrollable-result">' + result + '</div>', unsafe_allow_html=True)
                st.markdown("### Your Personalized Travel Plan")
                st.markdown(result)
                st.markdown("### Save Your Travel Plan")
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Travel Plan for {destination}</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                        h1, h2, h3 {{ color: #2c3e50; }}
                        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                        th {{ background-color: #f2f2f2; }}
                        tr:nth-child(even) {{ background-color: #f9f9f9; }}
                    </style>
                </head>
                <body>
                    <h1>Travel Plan for {destination}</h1>
                    <h2>Dates: {dates}</h2>
                    <div>{result}</div>
                </body>
                </html>
                """
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.download_button(
                        label="Download as Text",
                        data=result,
                        file_name=f"travel_plan_{destination.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                with col2:
                    st.download_button(
                        label="Download as Markdown",
                        data=result,
                        file_name=f"travel_plan_{destination.replace(' ', '_')}.md",
                        mime="text/markdown"
                    )
                with col3:
                    st.download_button(
                        label="Download as HTML",
                        data=html_content,
                        file_name=f"travel_plan_{destination.replace(' ', '_')}.html",
                        mime="text/html"
                    )
                with col4:
                    def generate_pdf_from_html(html_content, pdf_filename):
                        pdf = FPDF()
                        pdf.add_page()
                        pdf.set_auto_page_break(auto=True, margin=15)
                        pdf.set_font("Arial", size=12)
                        import re
                        text = re.sub('<[^<]+?>', '', html_content)
                        lines = text.split('\n')
                        for line in lines:
                            pdf.multi_cell(0, 10, line)
                        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                        pdf.output(temp_pdf.name)
                        temp_pdf.seek(0)
                        return temp_pdf
                    pdf_file = generate_pdf_from_html(html_content, f"travel_plan_{destination.replace(' ', '_')}.pdf")
                    with open(pdf_file.name, "rb") as f:
                        st.download_button(
                            label="Download as PDF",
                            data=f,
                            file_name=f"travel_plan_{destination.replace(' ', '_')}.pdf",
                            mime="application/pdf"
                        )
                with col5:
                    def generate_image_from_text(text, img_filename):
                        font_size = 16
                        font = None
                        try:
                            font = ImageFont.truetype("arial.ttf", font_size)
                        except:
                            font = ImageFont.load_default()
                        lines = text.split('\n')
                        width = 1200
                        line_height = font_size + 8
                        height = line_height * (len(lines) + 4)
                        img = Image.new('RGB', (width, height), color=(255,255,255))
                        d = ImageDraw.Draw(img)
                        y = 20
                        for line in lines:
                            d.text((20, y), line, font=font, fill=(0,0,0))
                            y += line_height
                        temp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
                        img.save(temp_img.name)
                        temp_img.seek(0)
                        return temp_img
                    img_file = generate_image_from_text(result, f"travel_plan_{destination.replace(' ', '_')}.png")
                    with open(img_file.name, "rb") as f:
                        st.download_button(
                            label="Download as Image",
                            data=f,
                            file_name=f"travel_plan_{destination.replace(' ', '_')}.png",
                            mime="image/png"
                        )
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.exception(e)
    else:
        st.info("Fill in your trip details in the sidebar and click 'Generate Travel Plan'.")

# --- App Routing Logic ---
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    authentication_page()
else:
    main_page()