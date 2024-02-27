import google.generativeai as genai
import time

# Assuming genai.configure is called outside the function, or you can include it in every call
genai.configure(api_key=" ")

last_request_time = None

def generate_corrected_email(email_text):
    global last_request_time

    # Check if we need to wait to respect the rate limit of 60 requests per minute
    if last_request_time is not None:
        time_since_last_request = time.time() - last_request_time
        wait_time = max(0, 1 - time_since_last_request)  # 1 second delay between requests as a simple rate-limiting strategy
        if wait_time > 0:
            time.sleep(wait_time)

    # Set up the model configuration
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]

    # Initialize the model with the specified configuration
    model = genai.GenerativeModel(model_name="gemini-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    # Define the prompt
    prompt_parts = [
        f"""Transform this: {email_text} into a more polished and effective pitch by correcting typographical errors and shorten the 3rd sentence with a max of 15 words make sure its email ready so dont put any footer or PS or other in your response like thanks , sincerely yours etc.
        JUST GIVE THE EMAIL DONT GIVE ME SUBJECT OR ETC IT HAS TO BE COPY PASTE READY."""
    ]

    # Generate content based on the prompt
    response = model.generate_content(prompt_parts)

    # Update the last request time
    last_request_time = time.time()

    return response.text

# Example usage
email_text = "This is the email text that needs correction."
corrected_email = generate_corrected_email(email_text)
print(corrected_email)
