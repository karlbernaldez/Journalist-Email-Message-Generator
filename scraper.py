import requests
import json
import spacy
import csv
import time

nlp = spacy.load("en_core_web_sm")

def correct_spacing(text):
    doc = nlp(text)
    corrected_text = " ".join([token.text for token in doc])
    return corrected_text

def parse_and_concatenate(response_text):
    lines = response_text.split('\n')  # Split the text into lines
    concatenated_content = []

    for line in lines:
        if 'content' in line:
            try:
                data = json.loads(line[5:])  # Load the JSON data from the line
                content = data.get('content', '')  # Extract the 'content' field
                concatenated_content.append(content)
            except json.JSONDecodeError:
                pass  # If a line is not valid JSON, we skip it

    return ' '.join(concatenated_content).replace("\\n", " ")

def watt_stream(link, max_attempts=5):
    data = {
        "model": "wp-watt-3.52-16k",
        "content": f"Give me the product name or title without the colon only and the best statement only and construct a sentence how you are impressed with the author's review in first person perspective 1 sentence only and make it like your talking to the author and mention the reason. Respond using format like this Product Name:()Statement:()Impression:(Im impressed with your review as it (Reason)) JUST SEND ME THE RESPONSE ONLY NO NEED FOR OTHER WORDS {link}"
    }
    headers = {
        "Authorization": "Bearer 8c8dd76a47f54bdda7d7efa14b0ada59"
    }

    for attempt in range(max_attempts):
        rsp = requests.post("https://beta.webpilotai.com/api/v1/watt/stream", json=data, headers=headers, stream=True)
        status_code = rsp.status_code

        if status_code == 200:
            # Success, return the response text
            time.sleep(6)
            return rsp.text, status_code
        elif status_code == 429:
            # Rate limit hit, wait for 1 minute before retrying
            print(f"Attempt {attempt + 1} of {max_attempts}: Rate limit hit. Waiting 1 minute before retrying...")
            time.sleep(60)
        else:
            # Other errors, return None
            print(f"Error: {status_code}")
            return None, status_code

    return None, 429  # Return None and 429 after all attempts fail

    
if __name__ == "__main__":
    # Open the output file once at the beginning of the script
    with open('final_data_with_missing.csv', 'r') as csv_file, open('final_data.csv', 'a', newline='', encoding='utf-8') as output_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader, None)  # Skip the header
        writer = csv.writer(output_file)  # Prepare the CSV writer for the output file

        for row in csv_reader:
            if row:
                link = row[0]
                print(link)

                text, code = watt_stream(link)

                while code == 429:
                    time.sleep(60)
                    text, code = watt_stream(link)

                if text:
                    final_content = parse_and_concatenate(text)
                    corrected_content = correct_spacing(final_content)
                    lines = corrected_content.strip().split('\n')
                    result = {}

                    # Iterate through the lines and extract key-value pairs
                    for line in lines:
                        if ':' in line:
                            key, _, value = line.partition(':')
                            result[key.strip()] = value.strip()

                    # Prepend the link to the row data
                    row_data = [link] + list(result.values())

                    # Write the data to CSV immediately after processing
                    if result:
                        writer.writerow(row_data)
                        print("Successful")
                    else:
                        # Write the link and a row of blanks if there's no output
                        writer.writerow([link] + [''] * len(result))
                        print("Blank")
                        print(text)
                else:
                    # If no text returned, write the link and a row of blanks
                    writer.writerow([link] + [''] * 3)
                    print("Failed to process link:", link)
