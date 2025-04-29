import streamlit as st
import pandas as pd
import os

# Assuming `analyze_sitemap.py` contains your analysis logic
from analyze_sitemap import analyze_sitemap  # Import your analysis function

def main():
    st.title("Sitemap SEO Analysis Tool")

    st.write("Welcome to the Sitemap SEO Analysis tool. Upload your sitemap and we will analyze it for SEO.")

    # File upload widget
    sitemap_file = st.file_uploader("Upload your Sitemap (.xml)", type=["xml"])

    if sitemap_file:
        # Save the uploaded file locally
        upload_path = os.path.join(os.getcwd(), "uploaded_sitemap.xml")
        with open(upload_path, "wb") as f:
            f.write(sitemap_file.getbuffer())

        st.write("Sitemap file uploaded successfully. Analyzing...")

        # Call your analysis function (this could be adjusted based on your code)
        result_df = analyze_sitemap(upload_path)

        # Display results in a table
        st.write("Analysis Results:")
        st.dataframe(result_df)

        # Optionally, you can allow users to download the results
        result_csv = result_df.to_csv(index=False)
        st.download_button("Download CSV", result_csv, file_name="sitemap_analysis.csv", mime="text/csv")

if __name__ == "__main__":
    main()
