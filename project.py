import google.generativeai as genai
import streamlit as st
import os

# Set your Google Cloud API key
api_key = "AIzaSyC4f-d-Igv6UWdHKoMgZcNfRTeQBFVgtUw"  # Replace with your actual API key
genai.configure(api_key=api_key)

# Create a temporary directory for uploaded images if it doesn't exist
if not os.path.exists("temp"):
    os.makedirs("temp")

# Streamlit UI setup
st.title("Food Calorie Estimator")
st.write("Upload an image of food items, and we'll estimate the calorie content.")

# Image uploader
image_file = st.file_uploader("Upload an image of food:", type=["jpg", "jpeg", "png"])

if image_file:
    # Provide the full path to save the uploaded image
    temp_image_path = os.path.join("temp", image_file.name)

    # Save the uploaded image to the temporary file
    with open(temp_image_path, "wb") as f:
        f.write(image_file.getbuffer())

    st.image(image_file, caption="Uploaded Image", use_column_width=True)

    # Button to generate calorie estimates
    if st.button("Estimate Calories"):
        try:
            # Upload the image to the Generative AI
            myfile = genai.upload_file(temp_image_path)
            # Removed the print statement for uploaded file info
            # st.write(f"Uploaded file: {myfile}")

            model = genai.GenerativeModel("gemini-1.5-flash")  # Replace with a valid model ID
            result = model.generate_content(
                [
                    myfile,
                    "\n\n",
                    """You are an expert nutritionist. provide the Breif explanation of the food and You do not need to provide exact calorie counts; you can give expected calorie ranges. Analyze the food items in this image and calculate the expected total calories.
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

    # Clean up the temporary file after processing
    if os.path.exists(temp_image_path):
        os.remove(temp_image_path)
