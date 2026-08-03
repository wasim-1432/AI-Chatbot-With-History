import streamlit as st
from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

# Configure API
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_recipe(ingredients, cuisine, diet):
    ''' 
        Generate a recipe using ingredients provided.
        Cuisine can be "Italian", "Mexican", "Indian", "Any", etc.
        Diet can be "Vegan", "Vegetarian","Jain","Any", etc.
    '''
    prompt = f'''
    You are an expert chef.

    Generate ONE food recipe using these ingredients: {', '.join(ingredients)}
    Rules:
    - Recipe should not be more than 100 words
    - Give Title, Ingredients list, and Steps clearly
    - Cuisine: {cuisine}
    - Diet: {diet}
    - If ingredients conflict with diet, suggest a substitute.

    Format in Markdown.
    '''

    response = client.models.generate_content(
        model="gemini-3.6-flash", # fixed model
        contents=prompt
    )
    return response.text

# --- Streamlit UI ---
st.set_page_config(page_title="AI Recipe Generator", page_icon="🍳")
st.title("🍳 AI Recipe Generator")
st.write("Enter your ingredients and get a recipe instantly!")

with st.sidebar:
    st.header("Settings")
    cuisine = st.selectbox("Cuisine", ["Any", "Indian", "Italian", "Mexican", "Chinese", "American", "Mediterranean"])
    diet = st.selectbox("Diet", ["Any", "Vegetarian", "Vegan", "Jain", "Non-Vegetarian", "Keto", "Gluten-Free"])
    # st.info("Make sure your GEMINI_API_KEY is set in .env file")

ingredients_input = st.text_input("Enter ingredients (comma separated)", placeholder="e.g. potato, tomato, paneer, rice")
ingredients_list = [i.strip() for i in ingredients_input.split(",") if i.strip()]

if st.button("Generate Recipe", type="primary"):
    if not ingredients_list:
        st.warning("Please enter at least one ingredient!")
    else:
        with st.spinner("Cooking up your recipe..."):
            try:
                recipe = generate_recipe(ingredients_list, cuisine, diet)
                st.markdown("### Your Recipe:")
                st.markdown(recipe)
            except Exception as e:
                st.error(f"Error: {e}")

st.caption("Built with Gemini + Streamlit")