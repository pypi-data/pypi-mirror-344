import subprocess
import os
import sys

# Function to start the Streamlit app
def run_streamlit():
    # Ensure Streamlit is installed
    try:
        import streamlit
    except ImportError:
        print("Streamlit is not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])

    # Run the Streamlit app by calling streamlit run from subprocess
    streamlit_app_path = os.path.join(os.path.dirname(__file__), 'streamlit_app.py')
    
    # Starting the Streamlit app
    subprocess.run(["streamlit", "run", streamlit_app_path])

# Main function to handle the script execution
def main():
    print("Starting the Streamlit app...")
    run_streamlit()

if __name__ == "__main__":
    main()
