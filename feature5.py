import streamlit as st
import datetime
import matplotlib.pyplot as plt
from groq import Groq

groq_api_key = "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"  # Replace with your actual API key
groq_client = Groq(api_key=groq_api_key)

def llama_model(prompt):
    """Utility to call the LLaMA model from Groq."""
    chat_completion = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.conten

st.title("Personalized Diet and Fitness Syncing App")

st.write("Fill in your details to get a tailored diet and fitness plan.")

age = st.number_input("Age", min_value=1, max_value=100, value=30)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
weight = st.number_input("Weight (kg)", min_value=20, max_value=200, value=70)
height = st.number_input("Height (cm)", min_value=100, max_value=250, value=165)
goal = st.selectbox("Diet Goal", ["Weight Loss", "Weight Gain", "Maintenance"])
activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
dietary_preferences = st.selectbox("Dietary Preferences", ["No Preference", "Vegetarian", "Vegan", "Low-Carb", "High-Protein"])
dietary_restrictions = st.multiselect("Dietary Restrictions", ["Gluten-Free", "Dairy-Free", "Nut-Free", "Shellfish-Free"])

time_frame_type = st.selectbox("Select Time Frame Type", ["Days", "Weeks", "Months"])
if time_frame_type == "Days":
    time_frame = st.number_input("Time Frame (in days)", min_value=1, max_value=365, value=7)
elif time_frame_type == "Weeks":
    time_frame = st.number_input("Time Frame (in weeks)", min_value=1, max_value=52, value=1) * 7  
else:
    time_frame = st.number_input("Time Frame (in months)", min_value=1, max_value=12, value=1) * 30 

calorie_goal = st.number_input("Daily Calorie Goal (kcal)", min_value=1000, max_value=5000, value=1800)

recent_workout_data = st.text_area("Enter recent workout data (e.g., duration, type, intensity):", "")
tracking_period = st.selectbox("Choose Tracking Period", ["Daily", "Weekly"])

hydration_goal = st.slider("Daily Hydration Goal (L)", min_value=1.0, max_value=5.0, value=2.5)

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
    - Goal: {goal}
    - Activity Level: {activity_level}
    - Dietary Preferences: {dietary_preferences}
    - Dietary Restrictions: {", ".join(dietary_restrictions)}
    - Time Frame: {time_frame} days
    - Daily Calorie Goal: {calorie_goal} kcal
    - Recent Workout Data: {recent_workout_data}
    - Daily Hydration Goal: {hydration_goal} L

    For each day of the time frame, provide:
    1. Detailed dietary recommendations, considering recent workout data and dietary restrictions.
    2. Breakdown of meals: breakfast, lunch, dinner, and snacks, with specific foods listed.
    3. Calorie and nutrient breakdown for each meal (e.g., protein, carbs, fats).
    4. Hydration goals and reminders.
    5. A summary of daily and weekly intake to help track calories and nutrient balance, including insights for {tracking_period} tracking.
    6. Provide tips on food choices and alternatives to reach the calorie goal.
    7. i want every day as i told you and suggest some food to me.

    Also, include a brief motivational tip for each day to help the user stay on track.
    """


    with st.spinner("Generating your personalized diet and fitness plan..."):
        try:
            plan = llama_model(prompt)
            st.success("Diet and fitness plan generated successfully!")
            st.write(plan)
        except Exception as e:
            st.error(f"An error occurred: {e}")
          
if tracking_period == "Weekly":
    st.header("Progress Overview")
    days = [f"Day {i}" for i in range(1, time_frame + 1)]
    calorie_intake = [calorie_goal + (i % 5 * 10 - 20) for i in range(time_frame)] 
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(days, calorie_intake, label="Daily Calorie Intake", marker="o", linestyle='-', color='b', markersize=8)
    ax.axhline(y=calorie_goal, color="r", linestyle="--", label="Target Calorie Goal")
    ax.set_xticks(range(len(days)))
    ax.set_xticklabels(days, rotation=45)
    ax.set_xlabel("Day", fontsize=14)
    ax.set_ylabel("Calories", fontsize=14)
    ax.set_title("Calorie Intake Progress", fontsize=16)
    ax.legend()
    ax.grid(True)
    plt.fill_between(days, calorie_intake, color='lightblue', alpha=0.5)
    st.pyplot(fig)
