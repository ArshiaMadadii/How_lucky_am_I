import streamlit as st
import pandas as pd
import random

# Function to load custom fonts
def load_custom_fonts():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&family=Poppins:wght@300;500&family=Lora:wght@400;700&display=swap');
            body {
                font-family: 'Roboto', sans-serif;
            }
            h1 {
                font-family: 'Poppins', sans-serif;
                font-weight: 700;
                color: #FFBF00;
                text-align: center;
            }
            h2 {
                font-family: 'Lora', serif;
                font-weight: 700;
                text-align: center;
                color: #333;
            }
            .main-title {
                text-align: center;
                font-family: 'Poppins', sans-serif;
                font-weight: 700;
                font-size: 40px;
            }
            .sub-title {
                text-align: center;
                font-family: 'Lora', serif;
                font-weight: 500;
                font-size: 30px;
                color: #333;
            }
            .statistics {
                font-family: 'Roboto', sans-serif;
                font-weight: 400;
                font-size: 18px;
                margin-top: 20px;
            }
            .github-instagram {
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 50px;
                margin-top: 50px;
            }
            .github-instagram a {
                font-family: 'Roboto', sans-serif;
                font-weight: 500;
                font-size: 18px;
                color: #333;
                text-decoration: none;
                display: flex;
                align-items: center;
            }
            .github-instagram a:hover {
                color: #FFBF00;
            }
            .github-instagram img {
                width: 40px;
                margin-right: 15px;
            }
            .dataframe {
                width: 100%;
                max-width: 100%;
                overflow: auto;
                border-radius: 15px;
                border: 1px solid #ddd;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                margin-bottom: 30px;
            }
            .dataframe th, .dataframe td {
                padding: 10px;
                text-align: center;
            }
            .dataframe th {
                background-color: #f7f7f7;
                color: #333;
                font-weight: 700;
            }
            .dataframe td {
                background-color: #fff;
                color: #555;
            }
        </style>
    """, unsafe_allow_html=True)

# Define initial dataset
def create_initial_dataset():
    check_frequency = [
        "Whenever I have a message", "Every two weeks", "Once a year", "Every six months", 
        "Whenever I have a message", "Whenever I have a message", "Every six months", 
        "Every three days", "Never", "Whenever I have a message", "Never", 
        "Whenever I have a message", "Whenever I have a message", "Rarely", 
        "Every three days", "Rarely", "Whenever I have a message", 
        "Every six months", "Whenever I have a message", "Every month", "Every week"
    ]

    response_probability = [
        "I don't reply", "30%", "I don't reply", "2%", 
        "I don't reply", "10%", "I don't reply", "I don't reply", 
        "I don't reply", "10%", "I don't reply", "10%", 
        "I reply to all", "I don't reply", "I don't reply", "I reply", 
        "I don't reply", "I reply to all", "I reply to all", 
        "20%", "10%"
    ]

    data = pd.DataFrame({
        "Check Frequency": check_frequency,
        "Response Probability": response_probability
    })
    return data

# Map qualitative data to numerical scores
def map_scores(data):
    check_frequency_scores = {
        "Whenever I have a message": 100,
        "Every three days": 80,
        "Every week": 60,
        "Every two weeks": 50,
        "Every month": 40,
        "Every six months": 20,
        "Once a year": 10,
        "Rarely": 5,
        "Never": 0
    }

    response_probability_scores = {
        "I reply to all": 100,
        "I reply": 75,
        "30%": 30,
        "20%": 20,
        "10%": 10,
        "2%": 2,
        "I don't reply": 0
    }

    data["Check Frequency Score"] = data["Check Frequency"].map(check_frequency_scores)
    data["Response Probability Score"] = data["Response Probability"].map(response_probability_scores)

    return data

# Calculate read probability
def calculate_read_probability(data):
    data["Read Probability"] = 0.7 * data["Check Frequency Score"] + 0.3 * data["Response Probability Score"]
    return data

# Generate random logical data
def generate_random_data(n):
    check_frequency_options = [
        "Whenever I have a message", "Every three days", "Every week", "Every two weeks", 
        "Every month", "Every six months", "Once a year", "Rarely", "Never"
    ]

    response_probability_options = [
        "I reply to all", "I reply", "30%", "20%", "10%", "2%", "I don't reply"
    ]

    random_data = []
    for _ in range(n):
        random_frequency = random.choice(check_frequency_options)
        random_response = random.choice(response_probability_options)
        random_data.append([random_frequency, random_response])

    random_df = pd.DataFrame(random_data, columns=["Check Frequency", "Response Probability"])
    return random_df

# Function to display two tables side by side with statistics
def display_side_by_side(data, random_data, combined_data):
    col1, col2 = st.columns(2)  # Create two columns

    # Left side - display the given dataset and success probability
    with col1:
        st.subheader("Given Dataset with Success Probability")
        st.dataframe(data, use_container_width=True)
        st.write("\nSuccess Probability Calculation")
        st.write("Calculated based on Check Frequency and Response Probability")

        # Display Initial Dataset Statistics below the table
        initial_avg_check_frequency = data["Check Frequency Score"].mean()
        initial_avg_response_probability = data["Response Probability Score"].mean()
        initial_avg_read_probability = data["Read Probability"].mean()

        st.write("\nInitial Dataset Statistics:")
        st.write(f"Average Check Frequency Score: {initial_avg_check_frequency}")
        st.write(f"Average Response Probability Score: {initial_avg_response_probability}")
        st.write(f"Average Read Probability: {initial_avg_read_probability}")

        # Display the Day-Specific Probabilities for the left side
        st.write("\nDay-Specific Probabilities for Initial Dataset:")
        initial_day_probabilities = calculate_day_probabilities(data)
        for day, prob in initial_day_probabilities.items():
            st.write(f"{day}: {prob:.2f}%")

    # Right side - display current data, random data, and success probability
    with col2:
        st.subheader("Current and Random Data with Success Probability")
        st.dataframe(random_data, use_container_width=True)
        st.write("\nSuccess Probability Calculation")
        st.write("Calculated based on Check Frequency and Response Probability")

        # Display statistics for the right side
        st.write("\nCombined Dataset Statistics:")
        combined_avg_check_frequency = combined_data["Check Frequency Score"].mean()
        combined_avg_response_probability = combined_data["Response Probability Score"].mean()
        combined_avg_read_probability = combined_data["Read Probability"].mean()

        st.write(f"Average Check Frequency Score: {combined_avg_check_frequency}")
        st.write(f"Average Response Probability Score: {combined_avg_response_probability}")
        st.write(f"Average Read Probability: {combined_avg_read_probability}")

        # Display Day-Specific Probabilities for the right side
        st.write("\nDay-Specific Probabilities for Combined Dataset:")
        combined_day_probabilities = calculate_day_probabilities(combined_data)
        for day, prob in combined_day_probabilities.items():
            st.write(f"{day}: {prob:.2f}%")

# Calculate day-specific probabilities
def calculate_day_probabilities(data):
    days = {
        "Day 1": 1,
        "Day 3": 3,
        "Day 7": 7,
        "Day 14": 14,
        "Day 30": 30,
        "Day 90": 90,
        "Day 180": 180
    }

    results = {}
    for day_name, day_value in days.items():
        decay_factor = max(0, 1 - (day_value / 365))  # Example decay model
        data[f"{day_name} Probability"] = data["Read Probability"] * decay_factor
        results[day_name] = data[f"{day_name} Probability"].mean()

    return results

# Main function to execute the process
def main():
    # Step 1: Load custom fonts
    load_custom_fonts()

    # Step 2: Create initial dataset
    data = create_initial_dataset()

    # Step 3: Map scores and calculate probabilities
    data = map_scores(data)
    data = calculate_read_probability(data)

    # Step 4: Generate random logical data
    random_data = generate_random_data(1000)
    random_data = map_scores(random_data)
    random_data = calculate_read_probability(random_data)

    # Step 5: Display headline with large font in yellow color at the top
    st.markdown("<h1>The ball is in your court now!</h1>", unsafe_allow_html=True)

    # Step 6: Display the new title with the updated text below the headline
    st.markdown("<h2 class='sub-title'>How likely is it that you've come this far?</h2>", unsafe_allow_html=True)

    # Step 7: Combine datasets for statistics
    combined_data = pd.concat([data, random_data], ignore_index=True)

    # Step 8: Display datasets and probabilities side by side
    display_side_by_side(data, random_data, combined_data)

    # Step 9: Add Instagram and GitHub Links with IDs at the bottom
    st.markdown("""
        <div class="github-instagram">
            <a href="https://www.instagram.com/arsh1amadadi/" target="_blank">
                <img src="https://upload.wikimedia.org/wikipedia/commons/9/95/Instagram_logo_2022.svg" alt="Instagram">
                @arsh1amadadi
            </a>
            <a href="https://github.com/arshiamadadii" target="_blank">
                <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" alt="GitHub">
                @arshiamadadii
            </a>
        </div>
    """, unsafe_allow_html=True)

# Run the main function
if __name__ == "__main__":
    main()
