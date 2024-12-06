import streamlit as st
import openai
import json
import pandas as pd

# Get the API key from the sidebar called OpenAI API key
user_api_key = st.sidebar.text_input("OpenAI API key", type="password")

# Check if the API key is provided
if user_api_key:
    # Set up OpenAI client
    openai.api_key = user_api_key
else:
    st.warning("Please provide an OpenAI API key in the sidebar.")

# Updated prompt for generating topic-based questions and answers
prompt = """You are an AI assistant capable of generating a list of questions based on a topic. 
You will receive a random topic. Your task is to:
1. Generate 10 questions about that topic.
2. Generate answers for all questions in a separate list.
3. Extract technical terms (e.g., important keywords, domain-specific terms, or capitalized words) from the questions and answers.
4. For each technical term, provide a brief description or explanation.

Return the result in JSON format with four parts:
- The first part is a JSON array of questions.
- The second part is a JSON array of answers.
- The third part is a JSON array of technical terms.
- The fourth part is a JSON array of descriptions for each technical term.
            """

st.title('Topic-Based Question Generator')
st.markdown('Enter a topic, and AI will generate questions and answers for you.')

# Text input for the topic
topic = st.text_area("Enter the topic here:", "Your topic here")

# Submit button for processing the topic
if st.button('Generate Questions and Answers'):
    if not user_api_key:
        st.error("Please enter your OpenAI API key before submitting.")
    else:
        try:
            # Define the conversation with the model
            messages_so_far = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": topic},
            ]
            
            # Get the response from OpenAI
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages_so_far
            )
            
            # Extract the result from the response
            st.markdown('**AI Response:**')
            json_response = response.choices[0].message.content

            # Try parsing the JSON response
            result = json.loads(json_response)
            
            # Get the questions, answers, and technical terms from the response
            questions = result.get('questions', [])
            answers = result.get('answers', [])
            technical_terms = result.get('technical_terms', [])
            descriptions = result.get('descriptions', [])
            
            if questions and answers:
                # Display the questions and answers
                st.markdown("### Questions:")
                for idx, question in enumerate(questions, 1):
                    st.markdown(f"**Q{idx}:** {question}")
                
                st.markdown("### Answers:")
                for idx, answer in enumerate(answers, 1):
                    st.markdown(f"**A{idx}:** {answer}")

                # Display the technical terms and descriptions in a table
                if technical_terms and descriptions:
                    st.markdown("### Technical Terms and Descriptions:")
                    # Create a DataFrame for displaying in table format
                    terms_df = pd.DataFrame({
                        "Technical Term": technical_terms,
                        "Description": descriptions
                    })
                    st.table(terms_df)
            else:
                st.warning("No questions or answers found. Please try again.")
        
        
        except json.JSONDecodeError as e:
            st.error(f"Error in parsing the JSON response: {e}")
        except KeyError as e:
            st.error(f"Missing expected key in the response: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
