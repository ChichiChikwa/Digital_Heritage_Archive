import streamlit as st
from pathlib import Path
import google.generativeai as genai

#from api_key_Korin import api_key

# Configure generative AI with API key
#genai.configure(api_key=api_key)
genai.configure(api_key=st.secrets["api_key"])
# Setup the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192
}

# Apply safety settings
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
]

# System prompt as string
system_prompt = """
As a highly skilled historian and anthropologist specializing in cultural heritage preservation, you are tasked with the following:

Your Responsibilities:

1.Detailed Analysis: Carefully examine each artifact, site, or cultural practice presented, focusing on historical context, significance, and preservation status. Analyze the cultural, social, and political dimensions that underpin the heritage item.
2.Cultural Significance Report: Document the origins, history, and cultural importance of each item or practice. Clearly articulate the connections to broader historical narratives or cultural phenomena.
3.Preservation Recommendations and Next Steps: Based on your analysis, suggest potential next steps for preservation, including immediate actions or long-term strategies to safeguard the heritage.
4.Community and Stakeholder Engagement Suggestions: If appropriate, recommend ways to involve local communities or stakeholders in the preservation process to ensure sustainable and respectful conservation practices.
Important Notes:

Scope of Response: Only respond to inquiries that pertain to cultural heritage items or practices.
Clarity of Documentation: In cases where the documentation or evidence is insufficient to conduct a thorough analysis, note that further research or field investigation may be necessary.
Disclaimer: Accompany your analysis with the disclaimer: "Recommendations for preservation should be implemented considering local laws, cultural sensitivities, and with the involvement of community stakeholders."
Your insights are invaluable in guiding efforts to preserve cultural heritage. Please proceed with the analysis.

"""

# Create the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Set up the Streamlit page
st.set_page_config(page_title="Cultural Heritage Recommendation System", page_icon=":arial:")
st.image("TajMahal.webp", width=200)
st.title("Cultural Heritage Recommendation System")
st.subheader("Helping users to preserve cultural heritage sites and practices")

# File uploader

uploaded_file = st.file_uploader("Upload an image of your heritage site", type=["png", "jpg", "jpeg"])
if uploaded_file:
    submit_button = st.button("Analyze Heritage Site")

    if submit_button:
        try:
            st.image(uploaded_file, width=300, caption="Uploaded Image")
            image_data = uploaded_file.getvalue()

            # Ensure the part for image is structured correctly
            image_parts = {"mime_type": "image/jpeg", "data": image_data}
            prompt_text = {"text": system_prompt}
            prompt_parts = [prompt_text, image_parts]

            response = model.generate_content({"parts": prompt_parts})
            st.image(image_data, width=400)
            st.write(response.text)
        except Exception as e:
            st.error(f"Failed to generate content: {str(e)}")

