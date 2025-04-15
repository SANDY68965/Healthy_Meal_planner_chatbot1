import streamlit as st
import requests

# 🔐 Spoonacular API setup
API_KEY = "0f025642be1a4cdb85b4b2912d064e66"  # Replace with your real API key
BASE_URL = "https://api.spoonacular.com/recipes/complexSearch"

# 🔁 Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "users" not in st.session_state:
    st.session_state.users = {"demo": "password123"}

# 🍽️ Recipe fetching function
def get_recipes(meal_type, diet, number=5):
    params = {
        "apiKey": API_KEY,
        "type": meal_type,
        "diet": diet,
        "number": number,
        "addRecipeInformation": True,
        "sort": "healthiness"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        st.error("❌ Failed to fetch recipes. Please check your API key and try again.")
        return []
    data = response.json()
    return [
        {"title": r["title"], "url": r.get("sourceUrl", "No URL available")}
        for r in data.get("results", [])
    ]

def login_ui():
    st.title("🔐 Login or Register")
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if username in st.session_state.users and st.session_state.users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("✅ Logged in successfully!")
                st.rerun()  # ✅ fixed here
            else:
                st.error("❌ Invalid username or password.")

    with tab2:
        new_user = st.text_input("New Username", key="reg_user")
        new_pass = st.text_input("New Password", type="password", key="reg_pass")
        if st.button("Register"):
            if new_user in st.session_state.users:
                st.warning("⚠️ Username already exists.")
            elif not new_user or not new_pass:
                st.warning("⚠️ Username and password cannot be empty.")
            else:
                st.session_state.users[new_user] = new_pass
                st.success("🎉 Registered! Please log in.")

# 🏠 Main App (after login)
def main_app():
    st.title("🥗 Healthy Meal Planner")
    st.markdown(f"Welcome, **{st.session_state.username}**! 👋")

    meal_type = st.selectbox("Select Meal Type", ["breakfast", "lunch", "dinner"])
    diet = st.selectbox("Select Dietary Preference", ["vegetarian", "vegan", "paleo", "keto", "gluten free"])

    if st.button("Find Recipes"):
        if not API_KEY.strip():
          st.error("❗ Please set a valid Spoonacular API key.")

        else:
            with st.spinner("🔍 Fetching recipes..."):
                recipes = get_recipes(meal_type, diet)
            if recipes:
                st.success(f"Found {len(recipes)} recipes:")
                for i, r in enumerate(recipes, 1):
                    st.markdown(f"**{i}. {r['title']}**  \n🔗 [View Recipe]({r['url']})")
            else:
                st.error("❌ No recipes found.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()


# 🧭 App routing
if st.session_state.logged_in:
    main_app()
else:

    login_ui()
