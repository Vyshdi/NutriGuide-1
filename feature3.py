import google.generativeai as genai
import streamlit as st
import os

api_key = "AIzaSyC4f-d-Igv6UWdHKoMgZcNfRTeQBFVgtUw"  # Replace with your actual API key
genai.configure(api_key=api_key)

if not os.path.exists("temp"):
    os.makedirs("temp")

st.title("Food Allergen Checker")
st.write("Check if a food dish contains any allergens you have or general allergens.")

# User input for food dish
food_item = st.text_input("Enter the food dish you want to check (e.g., Pizza):")

# User input for allergies
allergen = st.text_input("Enter any specific allergens if you have (optional) e.g., peanuts, garlic:")

# File uploader for food image
image_file = st.file_uploader("Upload a photo of the food dish (optional):", type=["jpg", "jpeg", "png"])

if st.button("Check Allergens"):
    # Initialize temp_image_path variable
    temp_image_path = None

    if food_item or image_file:
        # Construct the prompt to the model
        prompt = ""

        if allergen:
            if food_item:
                prompt += f"The dish '{food_item}' is being analyzed. I am allergic to '{allergen}'. Does this dish contain my allergen? Please provide a simple 'yes', 'no', 'high probability', or 'low chances', and 4-5 lines of explanation and also warning about avoiding to use '{allergen} in the dish"
            if image_file:
                # Save the uploaded image to a temporary file
                temp_image_path = os.path.join("temp", image_file.name)
                with open(temp_image_path, "wb") as f:
                    f.write(image_file.getbuffer())
                prompt += f"\nThis is the food '{temp_image_path}' I am going to eat. I am allergic to '{allergen}'. You don't have to determine the exact ingredients ,Just tell if generally the food dish can contain '{allergen}? First, give a one-word answer like 'Yes,' 'No,' 'May Contain,' or 'High Chance,' followed by a detailed explanation and also warning about avoiding to use '{allergen} in the dish."
        else:
            if food_item:
                prompt += f"Analyze the dish '{food_item}' for potential allergens. What ingredients might cause allergic reactions? Please provide a summary."
            if image_file:
                # Save the uploaded image to a temporary file
                temp_image_path = os.path.join("temp", image_file.name)
                with open(temp_image_path, "wb") as f:
                    f.write(image_file.getbuffer())
                prompt += f"\nThis is the food '{temp_image_path}' I am going to eat. What ingredients might cause allergic reactions? Please provide a summary."

        # AI Model Execution
        if prompt:  # Check if prompt is not empty
            model = genai.GenerativeModel("gemini-1.5-flash")
            try:
                if temp_image_path:  # Check if the image path is defined (i.e., an image was uploaded)
                    myfile = genai.upload_file(temp_image_path)  # Upload the image file for analysis
                    result = model.generate_content(
                        [
                            myfile,
                            "\n\n",
                            prompt,
                        ]
                    )
                else:
                    # If no image was uploaded, use the prompt without an image file
                    result = model.generate_content(prompt)

                # Display the result in a dedicated box
                # Extract the one-word response and explanation from the result
                response_lines = result.text.splitlines()
                simple_response = response_lines[0] if response_lines else "No response received."
                explanation = "\n".join(response_lines[1:]) if len(response_lines) > 1 else ""

                # Determine the box color based on the response
                if "yes" in simple_response.lower():
                    response_color = "#FF4D4D"  # More intense red for "Yes"
                elif "high probability" in simple_response.lower():
                    response_color = "#FF4D4D"  # More intense red for "High Probability"
                elif "no" in simple_response.lower():
                    response_color = "#ADD8E6"  # Light blue for "No"
                elif "low chances" in simple_response.lower():
                    response_color = "#B0E0E6"  # Light blue for "Low Chances"
                else:
                    response_color = "#D3D3D3"  # Light grey for unexpected responses

                # Display the simple response in a colored box
                st.success("Allergen check completed!")
                st.markdown(
                    f"<div style='border: 2px solid {response_color}; padding: 10px; border-radius: 5px; background-color: {response_color};'>Response: {simple_response}</div>",
                    unsafe_allow_html=True
                )

                # Display the detailed explanation in another box
                if explanation:
                    st.markdown(
                        f"<div style='border: 2px solid #2196F3; padding: 10px; border-radius: 5px;'><strong>Explanation:</strong><br>{result.text}</div>",
                        unsafe_allow_html=True
                    )

            except Exception as e:
                st.error(f"An error occurred during the allergen check: {e}")
        else:
            st.error("Unable to generate a prompt for the AI. Please check your inputs.")
    else:
        st.error("Please enter a food dish or upload a photo to check.")

    # Clean up the temporary image file after processing
    if temp_image_path and os.path.exists(temp_image_path):
        os.remove(temp_image_path)
