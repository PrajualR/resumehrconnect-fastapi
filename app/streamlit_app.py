import streamlit as st
import requests
import pandas as pd
import time

# Set page configuration
st.set_page_config(
    page_title="Resume-Job Description Matcher",
    page_icon="📄",
    layout="wide"
)


def main():
    # App title and description
    st.title("📄 Resume-Job Description Matcher")
    st.markdown("""
    Upload multiple resumes and a job description to find the best matches using BERT embeddings!
    """)

    # API endpoint URL - adjust this if your FastAPI is running on a different address
    api_url = "http://localhost:8000/match"

    # Create two columns for job description and file upload
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Job Description")
        job_description = st.text_area(
            "Enter the job description here:",
            height=300,
            placeholder="Paste the job description text here..."
        )

    with col2:
        st.subheader("Resume Upload")
        resume_files = st.file_uploader(
            "Upload resume PDFs:",
            type=["pdf"],
            accept_multiple_files=True
        )

    # Match button
    if st.button("Match Resumes", type="primary", disabled=not (job_description and resume_files)):
        if not job_description:
            st.error("Please enter a job description.")
        elif not resume_files:
            st.error("Please upload at least one resume.")
        else:
            with st.spinner("Matching resumes... This may take a moment."):
                try:
                    # Prepare the form data
                    files = [("resumes", (file.name, file.getvalue(), "application/pdf")) for file in resume_files]

                    # Send request to FastAPI
                    response = requests.post(
                        api_url,
                        data={"job_description": job_description},
                        files=files
                    )

                    # Check if request was successful
                    if response.status_code == 200:
                        results = response.json()

                        if results:
                            st.success(f"Successfully matched {len(results)} resumes!")

                            # Create a dataframe for better display
                            df = pd.DataFrame(results)

                            # Format the dataframe
                            if not df.empty:
                                df = df[["rank", "filename", "similarity_score"]]
                                df["similarity_score"] = df["similarity_score"].apply(lambda x: f"{x:.2%}")

                                # Display results
                                st.subheader("Ranked Resumes")
                                st.dataframe(df, use_container_width=True)

                                # Display each result with more details
                                st.subheader("Detailed Results")
                                for result in results:
                                    with st.expander(
                                            f"Rank {result['rank']}: {result['filename']} - Match: {result['similarity_score']:.2%}"):
                                        st.markdown("**Text Preview:**")
                                        st.text(result["preview"])
                            else:
                                st.warning("No matching results found.")
                        else:
                            st.warning("No results returned. The resumes may not be in a readable format.")
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.markdown("""
                    **Possible issues:**
                    - Make sure the FastAPI server is running (check the README for instructions)
                    - Check that the API URL is correct
                    - Ensure the resumes are valid PDF files
                    """)


if __name__ == "__main__":
    main()