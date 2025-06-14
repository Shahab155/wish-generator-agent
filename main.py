import streamlit as st
import os
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents.run import RunConfig
from dotenv import load_dotenv
import asyncio

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL= os.getenv("MODEL")

if not GEMINI_API_KEY or not BASE_URL or not MODEL:
    st.error("Please set API_KEY, or BASE_URL or, MODEL in .env file")
    st.stop()

client = AsyncOpenAI(
    base_url=BASE_URL,
    api_key=GEMINI_API_KEY
)

model = OpenAIChatCompletionsModel(
    model=MODEL,
    openai_client=client,
    
)

wish_generator_agent = Agent(
    name="Wish Generator",
    instructions="You are beautiful wishes generator.",
    model=model
)

config = RunConfig (
    model=model,
    model_provider=client,
    tracing_disabled=True
)

# Set the page configuration in streamlit
st.set_page_config(page_title="Wish Generator Agent",page_icon="🤖")

st.markdown("""
      <style>
            body {
            background-color: white;
            font-family: "Roboto", sans
            }

            .stApp {
           background: #780206;  /* fallback for old browsers */
           background: -webkit-linear-gradient(to right, #061161, #780206);  /* Chrome 10-25, Safari 5.1-6 */
           background: linear-gradient(to right, #061161, #780206); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */;
            font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
            }
         
            input {
            border-radius: 10px;
            border: 2px solid #080080;
            font-size:26px;
            color: white

            }
            .stTextInput>div>div>input {
            height:30px
            }

           .stButton > button {
            background-color: #0E2148;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            border:2px solid white
            
            }
          
          p {
            color:white
            }
                        
       </style>     
""",unsafe_allow_html=True)


st.markdown("<h1 style='text-align: center;color:white'>😎Wish Generator Agent🤖</h1>",unsafe_allow_html=True)
st.markdown("<h2 style='color:white'>Welcome to wish generator✨</h2>",unsafe_allow_html=True)
st.markdown("<p style='color:white'>This agent helps you create personalized wishes like Eid, Birthday, or Anniversary greetings — just tell it the type of wish you want!</p>",unsafe_allow_html=True)


name = st.text_input("Enter a name: ")
wish_type = st.selectbox("Select a wish type you want to generate",["Eid","Birthday","Anniversary","Wedding","Promotion","New Year","Good Morning"])
    
async def generate_wish(name, wish_type):
    result = await Runner.run(
         wish_generator_agent,
         f"Generate a {wish_type} wish for {name}, in a beautiful way and also include appropriate emojis for given wish type. Act as professional",
         run_config=config
        )    
    return result.final_output

if st.button("Generate Wish"):
    if name and wish_type:
        with st.spinner("Generating wish. please wait....."):
            final_message = asyncio.run(generate_wish(name, wish_type))
            st.text_area(f"Here is {wish_type} wish generated:", value=final_message, height=200)
            st.balloons()
    else:
        st.error("Please enter name and select a wish type.")

st.markdown("----") 
st.markdown("<h2 style='color:white; text-align: center'>Build with 💖 by Shahab</h2>",unsafe_allow_html=True)   
