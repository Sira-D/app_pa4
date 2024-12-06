import streamlit as st
import openai
import json

# Get the API key from the sidebar called OpenAI API key
user_api_key = st.sidebar.text_input("OpenAI API key", type="password")

# Set up OpenAI client
openai.api_key = user_api_key

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
    
    try:
        # Parse the JSON response
        result = json.loads(json_response)
        
        # Get the questions and answers from the response
        questions = result.get('questions', [])
        answers = result.get('answers', [])
        
        # Display the questions and answers
        if questions and answers:
            st.markdown("### Questions:")
            for idx, question in enumerate(questions, 1):
                st.markdown(f"**Q{idx}:** {question}")
            
            st.markdown("### Answers:")
            for idx, answer in enumerate(answers, 1):
                st.markdown(f"**A{idx}:** {answer}")
        else:
            st.warning("No questions or answers found.")
    
    except json.JSONDecodeError as e:
        st.error(f"Error in parsing the JSON response: {e}")
    except KeyError as e:
        st.error(f"Missing expected key in the response: {e}")
