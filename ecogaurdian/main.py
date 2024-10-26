import streamlit as st
import datetime
import pandas as pd
import joblib
import pyttsx3

# Sample function for loading a pre-trained model
def load_model():
    # Replace this with your actual model loading logic
    model = joblib.load("nrgforecast.pkl")
    return model

def compute_datetime_values(user_date, user_time):
    """Calculates various datetime-related values based on user input."""
    combined_datetime = datetime.datetime.combine(user_date, user_time)
    df = pd.DataFrame({
        "datetime": [combined_datetime],
        "dayofyear": [int(combined_datetime.strftime("%j"))],
        "hour": [int(combined_datetime.strftime("%H"))],
        "dayofweek": [combined_datetime.weekday()],  # 0 for Monday, 1 for Tuesday, ..., 6 for Sunday
        "quarter": [(combined_datetime.month - 1) // 3 + 1],
        "month": [int(combined_datetime.strftime("%m"))],
        "year": [int(combined_datetime.strftime("%Y"))]
    })
    return df

def speak_predictions(predictions):
    engine = pyttsx3.init()
    engine.say("The predicted production in megawatts is: " + str(predictions[0]))
    engine.runAndWait()

def main():
    st.title("🌿 Eco Guardian 🌍🛡️")

    # User input for date and time
    user_date = st.date_input("Select Date:")
    user_time = st.time_input("Select Time:")

    if st.button("Calculate"):
        # Calculate datetime-related values
        df_datetime = compute_datetime_values(user_date, user_time)

        # Load the model (replace with your actual model loading function)
        model = load_model()

        # Use the calculated values as input to the model
        model_input = df_datetime[['dayofyear', 'hour', 'dayofweek', 'quarter', 'month', 'year']]

        # Make predictions using the model
        predictions = model.predict(model_input)

        # Display model predictions
        st.subheader("Production in (MW)🌎🌱")
        st.write(predictions)

        # Speak out the predictions using pyttsx3
        speak_predictions(predictions)

if __name__ == "__main__":
    main()
