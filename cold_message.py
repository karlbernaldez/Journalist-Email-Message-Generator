import csv
from corrector import generate_corrected_email

# Define the email template
email_template = """
Hey {reviewer_first_name} again, 

I know you are super busy,  and there is a chance my pitch got buried in your inbox. I recently read your insightful article about {Product} on {publication_name}. {Impression}. 

I’d like to inquire if you are interested in reviewing and testing out our new product, Radiant, the world's first reflective LCD monitor – providing an alternative to E-paper. Our company specifically makes electronics to help with eye strain and discomfort and has been featured in many publications, including Creative Bloq, dextero, Fast Magazine, etc. Radiant is 70% more electricity-efficient, usable outdoors, and less straining on the eyes. Let me know if this interests you, and I’m happy to send over a unit immediately for you to look at.
"""

# Open the output CSV file for writing with UTF-8 encoding
with open('automation_data_with_emails.csv', 'w', newline='', encoding='utf-8') as output_csvfile:
    # Assume the input CSV has the header already, so we read it to determine field names
    with open('Radiant2.csv', newline='', encoding='utf-8') as input_csvfile:
        reader = csv.DictReader(input_csvfile)
        fieldnames = reader.fieldnames + ['Email Message', 'Raw Email'] # Add the new column for emails
        writer = csv.DictWriter(output_csvfile, fieldnames=fieldnames)
        writer.writeheader()  # Writes the header

        for row in reader:
            # Generate the email message for each row
            email_message = email_template.format(
                reviewer_first_name=row['First name'],
                Product=row['Product'],
                publication_name=row['Company name'],
                Impression=row['Impression'],
                Statement=row['Statement'],
            )
            
            # Assuming generate_corrected_email is a placeholder for actual correction logic
            corrected_email = generate_corrected_email(email_message)
            print(corrected_email)
            
            # Add the corrected email to the row
            row['Email Message'] = corrected_email
            row['Raw Email'] = email_message
            # Write the updated row to the CSV file
            writer.writerow(row)



