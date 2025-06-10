Step 1: Initialize the Environment
1. Load environment variables (like the API key) from .env file.
2. Import libraries:
○ streamlit for the frontend.
○ requests for API calls.
○ dotenv for loading environment variables.
○ time for exponential backoff in case of API rate limits.
Step 2: Frontend User Inputs
1. Display app title and description using streamlit components.
2. Layout options in columns:
○ Age Group selector (Child, Teen, Adult).
○ Historical Role selector (Explorer, Ruler, Scientist, Philosopher, Warrior).
3. Provide a text input field for the "What If" scenario.
4. Provide a button to trigger rewriting.
Step 3: Validate User Input
1. Check if the scenario is not empty.
2. If empty, display an error message.
3. If valid, proceed to generate alternate histories.
Step 4: Generate Prompt for API
1. Based on the age group:
○ Set the language style (e.g., child-friendly, teen-friendly, adult-friendly).
○ Set the length of the alternate history.
2. Based on the historical role, set the role description (e.g., “a scientist like
Newton”).
3. Combine the user scenario, role description, and language style into a prompt
that:
○ Summarizes the Original History.
○ Generates the Alternate History.
Step 5: Call the OpenRouter API
1. Prepare API request:
○ URL: https://openrouter.ai/api/v1/chat/completions
○ Headers: include Authorization, Content-Type, and custom headers.
○ JSON payload: includes the model, system instructions, and user prompt.
2. Send API request using requests.post().
3. Handle API errors:
○ Retry up to 3 times using exponential backoff for 429 Too Many Requests.
○ If failed, show error in the frontend.
Step 6: Parse the API Response
1. Extract the Original History and Alternate History from the response.
2. If API didn’t return expected sections, handle gracefully.
Step 7: Display Results in Frontend
1. Use two columns in Streamlit to display:
○ Original History
○ Alternate History
2. If there are errors, display them in the respective columns.
Step 8: Styling and UX Enhancements
1. Apply custom CSS to enhance layout and appearance.
2. Provide visual separators (e.g., ---) to distinguish sections.
Summary in Pseudo-code:
● START
● |
● |-- Load environment variables
● |-- Initialize frontend (Streamlit app)
● |-- Get user input: age group, historical role, scenario
● |-- Validate input
● |-- If valid:
● | |-- Generate prompt based on age group, role
● | |-- Create API request (headers, payload)
● | |-- Send request to OpenRouter API
● | |-- If successful:
● | |-- Parse Original and Alternate History
● | |-- Display both in Streamlit
● | |-- If failed:
● | |-- Show error message
● |-- Else:
● | |-- Show input error message
● |
● END
