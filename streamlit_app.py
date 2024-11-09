import streamlit as st
import datetime
import os
import matplotlib.pyplot as plt
from groq import Groq  # Ensure 'groq' is available in your environment

# Attempt to import google-generativeai with error handling
try:
    import google.generativeai as genai
    genai_available = True
except ImportError:
    genai_available = False

st.title("NutriGuide")
st.write("This app analyzes nutritional information.")

# Check if genai is available before using it
if genai_available:
    st.write("Using Google Generative AI capabilities...")
    # Add code that uses `genai` here
else:
    st.write("Google Generative AI features are disabled.")

# Rest of your app code without references to `genai` outside this block

API_KEY_GROQ = "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"
API_KEY_GENAI = "AIzaSyC4f-d-Igv6UWdHKoMgZcNfRTeQBFVgtUw"

client = Groq(api_key=API_KEY_GROQ)
genai.configure(api_key=API_KEY_GENAI)

if not os.path.exists("temp"):
    os.makedirs("temp")

st.markdown("""
    <style>
    .main-bg {
        background-color: #F7F9FC;
        padding: 10px;
        border-radius: 8px;
    }
    .header-bg {
        color: #FFFFFF;
        background-color: #4C9F70;
        padding: 20px;
        text-align: center;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .feature-bg {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .btn-custom {
        background-color: #4C9F70;
        color: #FFFFFF;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)
st.markdown('<div class="header-bg"><h1>NutriGuide.AI - Your Personal Health and Diet Assistant</h1></div>', unsafe_allow_html=True)


st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox("Choose a feature", 
                                ["Personalized Meal Plan", 
                                 "Food Calorie Estimator", 
                                 "Food Allergen Checker", 
                                 "Diet Recommendation for Chronic Conditions",
                                 "Personalized Diet and Fitness Syncing"])

# Feature 1: Personalized Meal Plan
if app_mode == "Personalized Meal Plan":
    st.markdown('<div class="feature-bg"><h2>Personalized Meal Plan</h2></div>', unsafe_allow_html=True)

    
    age = st.number_input("Enter your age:", min_value=0, max_value=120)
    sex = st.selectbox("Select your sex:", ["Male", "Female", "Other"])
    weight_goal = st.selectbox("Weight goal:", ["Gain", "Loss"])
    eating_habits = st.selectbox("Eating habits:", ["Omnivore", "Flexitarian", "Pescatarian", "Vegetarian", "Vegan"])
    dietary_restrictions = st.selectbox("Dietary restrictions:", ["None", "Mediterranean", "Paleo", "Whole30", "Low Carb", "High Carb", "Gluten-Free", "Lactose-Free", "Raw Food", "Alkaline Food"])
    intermittent_fast_timing = st.selectbox("Select your intermittent fasting schedule:", ["None", "16/8", "18/6", "20/4"])
    traditional_diet = st.selectbox("Choose traditional diet:", ["None", "Ayurvedic", "Macrobiotic", "Halal", "Kosher"])
    duration = st.selectbox("Meal plan duration:", ["One day", "One week", "One month"])

    if st.button("Get Meal Plan", key="meal_plan_btn"):
        try:
            messages = [
                {
                    "role": "user",
                    "content": f"Write a personalized meal generation for the following parameters\n"
                               f"1. Age: {age}\n"
                               f"2. Sex: {sex}\n"
                               f"3. Weight goal: {weight_goal}\n"
                               f"4. Food eating habits: {eating_habits}\n"
                               f"5. Dietary restrictions: {dietary_restrictions}\n"
                               f"6. Intermittent fasting :{intermittent_fast_timing}\n"
                               f"7. Traditional diet: {traditional_diet}\n"
                               f"8. duration :{duration}\n"
                },
                {
                    "role": "assistant",
                    "content":"dont inlucde to consult wiht dietictian message ,start with your personlized meal plan is\n"
                              "Provide a meal plan based on the above parametersand also include the cost of the meals in INR\n"
                              "make sure first the dish must be mentioned followed by ingeredints and its cost then approximation of entire dish\n"
                              "when its intermittent fasting make sure to take time which user provides\n"
                              "provide deatils of the paramter choosen by the user before giving the diet \n"

                }
            ]
            completion = client.chat.completions.create(
                model="llama-3.2-90b-text-preview",
                messages=messages,
                temperature=1,
                max_tokens=1024
            )
            meal_plan = completion.choices[0].message.content
            st.write(meal_plan)
        except Exception as e:
            st.error(f"Error: {e}")

# Feature 2: Food Calorie Estimator
elif app_mode == "Food Calorie Estimator":
    st.markdown('<div class="feature-bg"><h2>Food Calorie Estimator</h2></div>', unsafe_allow_html=True)
    image_file = st.file_uploader("Upload a food image for calorie estimation:", type=["jpg", "jpeg", "png"])

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
            finally:
                os.remove(temp_image_path)

# Feature 3: Food Allergen Checker
elif app_mode == "Food Allergen Checker":
    st.markdown('<div class="feature-bg"><h2>Food Allergen Checker</h2></div>', unsafe_allow_html=True)
    food_item = st.text_input("Enter the food dish you want to check (e.g., Pizza):")
    allergen = st.text_input("Enter any specific allergens if you have (optional):")
    image_file = st.file_uploader("Upload an image of the food dish (optional):", type=["jpg", "jpeg", "png"])

    if st.button("Check Allergens"):
        temp_image_path = None  # Initialize variable for temporary image path
        if food_item or image_file:
            prompt = ""
            if allergen:
                if food_item:
                    prompt += f"The dish '{food_item}' is being analyzed. I am allergic to '{allergen}'. Does this dish contain my allergen? Please provide a simple 'yes', 'no', 'high probability', or 'low chances', and 4-5 lines of explanation with a warning about avoiding '{allergen}' in the dish."
                if image_file:
                    temp_image_path = os.path.join("temp", image_file.name)
                    with open(temp_image_path, "wb") as f:
                        f.write(image_file.getbuffer())
                    prompt += f"\nThis is the food '{temp_image_path}' I am going to eat. I am allergic to '{allergen}'. Just tell if the dish can generally contain '{allergen}'. Give a one-word answer followed by a detailed explanation."
            else:
                if food_item:
                    prompt += f"Analyze the dish '{food_item}' for potential allergens. What ingredients might cause allergic reactions? Please provide a summary."
                if image_file:
                    temp_image_path = os.path.join("temp", image_file.name)
                    with open(temp_image_path, "wb") as f:
                        f.write(image_file.getbuffer())
                    prompt += f"\nThis is the food '{temp_image_path}' I am going to eat. What ingredients might cause allergic reactions? Please provide a summary."

            # Execute AI model
            if prompt:
                model = genai.GenerativeModel("gemini-1.5-flash")
                try:
                    if temp_image_path:
                        myfile = genai.upload_file(temp_image_path)
                        result = model.generate_content([myfile, "\n\n", prompt])
                    else:
                        result = model.generate_content(prompt)
                    
                    response_lines = result.text.splitlines()
                    simple_response = response_lines[0] if response_lines else "No response received."
                    explanation = "\n".join(response_lines[1:]) if len(response_lines) > 1 else ""

                    # Display responses in colored boxes
                    if "yes" in simple_response.lower():
                        response_color = "#FF4D4D"
                    elif "high probability" in simple_response.lower():
                        response_color = "#FF4D4D"
                    elif "no" in simple_response.lower():
                        response_color = "#ADD8E6"
                    elif "low chances" in simple_response.lower():
                        response_color = "#B0E0E6"
                    else:
                        response_color = "#D3D3D3"

                    st.success("Allergen check completed!")
                    st.markdown(
                        f"<div style='border: 2px solid {response_color}; padding: 10px; border-radius: 5px; background-color: {response_color};'>Response: {simple_response}</div>",
                        unsafe_allow_html=True
                    )
                    if explanation:
                        st.markdown(
                            f"<div style='border: 2px solid #2196F3; padding: 10px; border-radius: 5px;'><strong>Explanation:</strong><br>{explanation}</div>",
                            unsafe_allow_html=True
                        )
                except Exception as e:
                    st.error(f"An error occurred during the allergen check: {e}")
                finally:
                    if temp_image_path and os.path.exists(temp_image_path):
                        os.remove(temp_image_path)
            else:
                st.error("Unable to generate a prompt for the AI. Please check your inputs.")
        else:
            st.error("Please enter a food dish or upload a photo to check.")

# Feature 4: Diet Recommendation for Chronic Conditions
elif app_mode == "Diet Recommendation for Chronic Conditions":
    st.markdown('<div class="feature-bg"><h2>Diet Recommendation for Chronic Conditions</h2></div>', unsafe_allow_html=True)

    condition = st.text_input("Enter your chronic condition (e.g., Diabetes, Hypertension):")
    severity = st.selectbox("Select the severity level:", ["Mild", "Moderate", "Severe"])
    goals = st.text_input("Health goals related to this condition (e.g., lower blood pressure, manage blood sugar)")
    food = st.selectbox("What type of meal do you like?", ["Veg", "Non-Veg", "Vegan"])

    if st.button("Get Diet Recommendation"):
        try:
            messages = [
                {
                    "role": "user",
                    "content": (
                        f"Provide detailed information for {condition},{severity},{goals}{food}.\n"
                        "1. Conditional-specific nutritional guidelines\n"
                        "2. Customized meal planning. Include options for day, week, or month.\n"
                        "3. Symptom management tips\n"
                        "4. Educational content and lifestyle tips.\n"
                        "Please format the response accordingly."
            )
                }
            ]
            completion = client.chat.completions.create(
                model="llama-3.2-90b-text-preview",
                messages=messages,
                temperature=1,
                max_tokens=1024
            )
            diet_recommendation = completion.choices[0].message.content
            st.write(diet_recommendation)
        except Exception as e:
            st.error(f"Error: {e}")

# Feature 5: Personalized Diet and Fitness Syncing
elif app_mode == "Personalized Diet and Fitness Syncing":
    st.markdown('<div class="feature-bg"><h2>Personalized Diet and Fitness Syncing</h2></div>', unsafe_allow_html=True)
    # User Inputs
    age = st.number_input("Age", min_value=1, max_value=100, value=30)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    weight = st.number_input("Weight (kg)", min_value=20, max_value=200, value=70)
    height = st.number_input("Height (cm)", min_value=100, max_value=250, value=165)
    body_fat_percentage = st.number_input("Body Fat Percentage (%)", min_value=1, max_value=50, value=20)
    sleep_hours = st.number_input("Average Sleep Hours per Night", min_value=1, max_value=24, value=7)
    stress_level = st.selectbox("Stress Level", ["Low", "Medium", "High"])
    
    goal = st.selectbox("Diet Goal", ["Weight Loss", "Weight Gain", "Maintenance"])
    activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
    
    # New Nutritional Inputs
    protein_goal = st.number_input("Daily Protein Goal (g)", min_value=10, max_value=300, value=100)
    carb_goal = st.number_input("Daily Carbohydrate Goal (g)", min_value=20, max_value=500, value=250)
    fat_goal = st.number_input("Daily Fat Goal (g)", min_value=10, max_value=200, value=70)
    
    # Dietary Preferences & Restrictions
    dietary_preferences = st.selectbox("Dietary Preferences", ["No Preference", "Vegetarian", "Vegan", "Low-Carb", "High-Protein"])
    dietary_restrictions = st.multiselect("Dietary Restrictions", ["Gluten-Free", "Dairy-Free", "Nut-Free", "Shellfish-Free"])
    
    # Time Frame
    time_frame_type = st.selectbox("Select Time Frame Type", ["Days", "Weeks", "Months"])
    if time_frame_type == "Days":
        time_frame = st.number_input("Time Frame (in days)", min_value=1, max_value=365, value=7)
    elif time_frame_type == "Weeks":
        time_frame = st.number_input("Time Frame (in weeks)", min_value=1, max_value=52, value=1) * 7  
    else:
        time_frame = st.number_input("Time Frame (in months)", min_value=1, max_value=12, value=1) * 30 

    calorie_goal = st.number_input("Daily Calorie Goal (kcal)", min_value=1000, max_value=5000, value=1800)
    
    # Recent workout data
    recent_workout_data = st.text_area("Enter recent workout data (e.g., duration, type, intensity):", "")
    
    # Hydration Goal
    hydration_goal = st.slider("Daily Hydration Goal (L)", min_value=1.0, max_value=5.0, value=2.5)
    
    # Tracking Period input
    tracking_period = st.selectbox("Choose Tracking Period", ["Daily", "Weekly"])  # Ensure this is defined before being used in prompt
    
    # Motivation Tips
    st.sidebar.header("Daily Motivational Tip")
    motivational_tips = [
        "Stay consistent! Small progress adds up.",
        "Remember to rest and recover.",
        "Hydrate! Water is key to wellness.",
        "Take it one day at a time, you've got this!",
        "Celebrate small victories!",
    ]
    st.sidebar.write(motivational_tips[datetime.datetime.now().day % len(motivational_tips)])
    
    if st.button("Generate Diet and Fitness Plan"):
        prompt = f"""
        You are a nutrition and fitness expert. Based on the following information, create a detailed personalized diet and fitness plan:
        - Age: {age}
        - Gender: {gender}
        - Weight: {weight} kg
        - Height: {height} cm
        - Body Fat Percentage: {body_fat_percentage}%
        - Sleep: {sleep_hours} hours per night
        - Stress Level: {stress_level}
        - Goal: {goal}
        - Activity Level: {activity_level}
        - Dietary Preferences: {dietary_preferences}
        - Dietary Restrictions: {", ".join(dietary_restrictions)}
        - Time Frame: {time_frame} days
        - Daily Calorie Goal: {calorie_goal} kcal
        - Protein Goal: {protein_goal} g
        - Carbohydrate Goal: {carb_goal} g
        - Fat Goal: {fat_goal} g
        - Recent Workout Data: {recent_workout_data}
        - Daily Hydration Goal: {hydration_goal} L
        
        For each day of the time frame, provide:
        1. Detailed dietary recommendations, considering recent workout data and dietary restrictions.
        2. Breakdown of meals: breakfast, lunch, dinner, and snacks, with specific foods listed.
        3. Calorie and nutrient breakdown for each meal (e.g., protein, carbs, fats).
        4. Hydration goals and reminders.
        5. A summary of daily and weekly intake to help track calories and nutrient balance, including insights for {tracking_period} tracking.
        6. Provide tips on food choices and alternatives to reach the calorie goal.
        7. Suggest food alternatives based on available ingredients and preferences.
        8. Include a brief motivational tip for each day to help the user stay on track.
        """
        with st.spinner("Generating your personalized diet and fitness plan..."):
            try:
                # Use Groq client to generate the plan
                messages = [{"role": "user", "content": prompt}]
                completion = client.chat.completions.create(
                    model="llama-3.2-90b-text-preview",
                    messages=messages,
                    temperature=1,
                    max_tokens=1024
                )
                plan = completion.choices[0].message.content
                st.success("Diet and fitness plan generated successfully!")
                st.write(plan)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    
    # Visualize Calorie Intake (Weekly)
    if tracking_period == "Weekly":
        st.header("Progress Overview")
        days = [f"Day {i}" for i in range(1, time_frame + 1)]
        calorie_intake = [calorie_goal + (i % 5 * 10 - 20) for i in range(time_frame)] 
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(days, calorie_intake, label="Calorie Intake", color='blue', marker='o')
        ax.set_xlabel("Days")
        ax.set_ylabel("Calories (kcal)")
        ax.set_title("Weekly Calorie Intake")
        ax.legend()
        st.pyplot(fig)
