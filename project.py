import google.generativeai as genai
import streamlit as st
import os

api_key = "AIzaSyC4f-d-Igv6UWdHKoMgZcNfRTeQBFVgtUw"  # Replace with your actual API key
genai.configure(api_key=api_key)

if not os.path.exists("temp"):
    os.makedirs("temp")

st.title("Food Calorie Estimator")
st.write("Upload an image of food items, and we'll estimate the calorie content.")

image_file = st.file_uploader("Upload an image of food:", type=["jpg", "jpeg", "png"])

if image_file:
    temp_image_path = os.path.join("temp", image_file.name)
    with open(temp_image_path, "wb") as f:
        f.write(image_file.getbuffer())

    st.image(image_file, caption="Uploaded Image", use_column_width=True)
    if st.button("Estimate Calories"):
        try:
            myfile = genai.upload_file(temp_image_path)
            model = genai.GenerativeModel("gemini-1.5-flash") 
            result = model.generate_content(
                [
                    myfile,
                    "\n\n",
                    """You are an expert nutritionist.tell the food name, provide the Breif explanation of the food and You do not need to provide exact calorie counts; you can give expected calorie ranges. Analyze the food items in this image and calculate the expected total calories.
                    Also, provide details of every food item with its expected calorie intake range in the following format:

                    1. Item 1 - Expected calorie range (e.g., 100-150 calories)
                    2. Item 2 - Expected calorie range (e.g., 200-250 calories)
                    ...
                    
                    Finally, provide the total expected calorie range for all the items in the image.""",
                ]
            )

            st.success("Calorie estimation completed!")
            st.write(result.text)

        except Exception as e:
            st.error(f"An error occurred: {e}")

    if os.path.exists(temp_image_path):
        os.remove(temp_image_path)
