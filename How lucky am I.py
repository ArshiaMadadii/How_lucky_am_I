import streamlit as st
import pandas as pd
import random
import http.server
import socketserver
import os

# Define PORT and DIRECTORY for server
PORT = 8501
DIRECTORY = "."

# Custom HTTP handler to serve files
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
        return super().do_GET()

# Run HTTP server
with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()

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

# Function to display tables side by side with statistics
def display_side_by_side(data, random_data, combined_data):
    col1, col2 = st.columns(2)
    
    # Left side - display the given dataset
    with col1:
        st.subheader("Given Dataset with Success Probability")
        st.dataframe(data)
        st.write("\nSuccess Probability Calculation")
        st.write("Calculated based on Check Frequency and Response Probability")
        st.write("\nInitial Dataset Statistics:")
        st.write(f"Average Check Frequency Score: {data['Check Frequency Score'].mean()}")
        st.write(f"Average Response Probability Score: {data['Response Probability Score'].mean()}")
        st.write(f"Average Read Probability: {data['Read Probability'].mean()}")

    # Right side - display current data, random data, and success probability
    with col2:
        st.subheader("Current and Random Data with Success Probability")
        st.dataframe(random_data)
        st.write("\nSuccess Probability Calculation")
        st.write("Calculated based on Check Frequency and Response Probability")
        st.write("\nCombined Dataset Statistics:")
        st.write(f"Average Check Frequency Score: {combined_data['Check Frequency Score'].mean()}")
        st.write(f"Average Response Probability Score: {combined_data['Response Probability Score'].mean()}")
        st.write(f"Average Read Probability: {combined_data['Read Probability'].mean()}")
        
# Main function to execute the process
def main():
    load_custom_fonts()
    data = create_initial_dataset()
    data = map_scores(data)
    data = calculate_read_probability(data)
    
    random_data = generate_random_data(1000)
    random_data = map_scores(random_data)
    random_data = calculate_read_probability(random_data)

    combined_data = pd.concat([data, random_data], ignore_index=True)

    display_side_by_side(data, random_data, combined_data)

# Run the main function
if __name__ == "__main__":
    main()
