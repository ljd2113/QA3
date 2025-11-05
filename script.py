import requests
import json
from datetime import datetime, timedelta
# Import the necessary libraries for Step 3: Sending the Email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from openai import OpenAI
#This block is where the script imports all the essential Python libraries required to perform


# --- Configuration ---

NEWS_API_KEY = " "

SENDER_EMAIL = "ljdial2113@gmail.com"

SENDER_PASSWORD = "onbn oril leur rnzm"

RECIPIENT_EMAIL = "ljdial2113@gmail.com"

SMTP_SERVER = "smtp.gmail.com" # Use 'smtp.outlook.com' for Outlook/Hotmail

SMTP_PORT = 587

#this block is where the user sets up congifuration for sending and receiving email newsletters

# --- NEW: Add your OpenAI API Key for Step 2 ---

OPENAI_API_KEY = " "



TOPIC_OF_INTEREST = "artificial intelligence" # The search query

NUM_ARTICLES = 5



# --- NEW: Initialize the OpenAI client here (Crucial for connecting to OpenAI) ---

client = OpenAI(api_key=OPENAI_API_KEY)

#confirms your identity and opens the channel for communication with the AI.



# =========================================================================

# STEP 1: Fetch the Articles Function

# =========================================================================

def fetch_articles(topic, api_key, count):

    """Fetches the latest news articles for a given topic."""

    print(f"📰 Starting article fetch for topic: '{topic}'...")



    # Define the date range (e.g., articles from the last 24 hours)

    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    today = datetime.now().strftime('%Y-%m-%d')



    # News API 'everything' endpoint URL

    url = "https://newsapi.org/v2/everything"

   #this is the web address to grab info on all news articles

    # Parameters for the API request

    params = {

        'q': topic,

        'apiKey': api_key,

        'language': 'en',

        'sortBy': 'publishedAt', # Get the latest articles first

        'from': yesterday,

        'to': today,

        'pageSize': count # Limit to the number of articles we want

    }

#This function handles the data collection step for the articles

    try:

        response = requests.get(url, params=params)

        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)

        data = response.json()

       # this is for data retrieval and a quality check for the news articles

        # Check if the API returned any articles

        if data['status'] == 'ok' and data['totalResults'] > 0:

            print(f"✅ Successfully fetched {len(data['articles'])} articles.")

            return data['articles']

        else:

            print("❌ No articles found for the specified topic and date range.")

            return []

           # This block checks if news articles were successfuly retrieved from the API

    except requests.exceptions.RequestException as e:

        print(f"🚨 Error during API request: {e}")

        return []


#This block is the dedicated safety net for internet and connection errors.




# =========================================================================

# STEP 2: Summarize the Articles Function (NEW)

# =========================================================================

def summarize_article(content):

    """Uses the OpenAI API to summarize a piece of content."""

    if not content:

        return "No content available to summarize."



    # Prompt Engineering for a clear, concise summary

    prompt = f"""

    You are a professional news editor. Summarize the following article content into a very concise,

    email-friendly summary of no more than 3 bullet points. Focus only on the main, high-level takeaways.



    ARTICLE CONTENT:

    ---

    {content}

    ---

    """
#where you define the exact task and output format
   

    try:

        response = client.chat.completions.create(

            model="gpt-3.5-turbo",

            messages=[

                {"role": "user", "content": prompt}

            ],

            temperature=0.3 # Low temperature for factual, consistent summaries

        )

       

        summary = response.choices[0].message.content

        return summary

       #This portion extracts the summary from the AI's response and returns it, making the article ready for the email step.

    except Exception as e:

        # This catches errors like invalid API key or rate limits

        print(f"🚨 Error during LLM summarization: {e}")

        return "LLM summarization failed."



# =========================================================================

# STEP 3: Send an Email Function (NEW)

# =========================================================================

def send_newsletter(items, sender, password, recipient, smtp_server, smtp_port, topic):

    """Formats and sends the newsletter via email."""

   #The final step that sends the summarized news to the email address

    # --- 1. Construct the HTML Email Body ---

   

    html_body = f"""

    <html>

    <head>

        <style>

            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}

            .container {{ max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }}

            .article {{ margin-bottom: 25px; padding: 15px; background-color: #f9f9f9; border-left: 5px solid #007bff; }}

            h2 {{ color: #007bff; margin-top: 0; }}

            ul {{ padding-left: 20px; margin-top: 5px; }}

            li {{ margin-bottom: 5px; }}

            .footer {{ margin-top: 30px; font-size: 0.8em; color: #777; text-align: center; }}

        </style>

    </head>

    <body>

        <div class="container">

            <h1>🧠 AI-Powered News Digest: {topic.title()}</h1>

            <p>Here are the latest {len(items)} summarized articles from reliable sources:</p>

    """

   #This block is for designing and structuring the look and feel of the final newsletter email.

    # Add each article's summary, title, and link

    for item in items:

        # Replace newlines with HTML breaks for formatting

        summary_html = item['summary'].replace('\n', '<br>')

       

        html_body += f"""

        <div class="article">

            <h2>{item['title']}</h2>

            <p>{summary_html}</p>

            <p><a href="{item['url']}" style="color: #007bff; text-decoration: none; font-weight: bold;">Read the Full Article &rarr;</a></p>

        </div>

        """

       

    html_body += """

            <div class="footer">

                This newsletter was automatically generated using Python, News API, and OpenAI LLM.

            </div>

        </div>

    </body></html>

    """

   #this block generates the HTML code for each individual article and the email footer

    # --- 2. Create the Email Message Object ---

    msg = MIMEMultipart('alternative')

    msg['From'] = sender

    msg['To'] = recipient

    msg['Subject'] = f"Daily AI News Digest - {datetime.now().strftime('%Y-%m-%d')}"

   

    # Attach the HTML body to the email

    msg.attach(MIMEText(html_body, 'html'))

   

    # --- 3. Send the Email via SMTP ---

    try:

        # Connect to the SMTP server (secure connection)

        with smtplib.SMTP(smtp_server, smtp_port) as server:

            server.starttls()  # Upgrade the connection to a secure TLS connection

            server.login(sender, password)

            server.send_message(msg)

        print(f"✅ Successfully sent newsletter to {recipient}!")

       

    except Exception as e:

        print(f"🚨 Error sending email: {e}")

        print("Please check your email address, app password, and SMTP settings.")

#This part connects to the email server and checks for connection errors

# =========================================================================

# MAIN EXECUTION BLOCK (Updated for Step 2)

# =========================================================================

if __name__ == "__main__":

    articles_data = fetch_articles(TOPIC_OF_INTEREST, NEWS_API_KEY, NUM_ARTICLES)

   

    if articles_data:

        # Prepare a list of dictionaries to hold the refined data

        newsletter_items = []



        print("\n--- TEST OUTPUT: Headlines and Links ---")

        for i, article in enumerate(articles_data):

            item = {

                'title': article.get('title'),

                # News API often uses 'description' as a snippet, which we pass to the LLM.

                'content_to_summarize': article.get('description') or article.get('content') or "",

                'url': article.get('url'),

                'summary': "" # Placeholder for the summarized text

            }

            newsletter_items.append(item)

           

            # 1. Test by printing the headlines and article links.

            print(f"[{i+1}] Title: {item['title']}")

            print(f"    Link: {item['url']}")

#this is the starting point where they call functions in order
           

        print("---------------------------------------")

       #verifies that the articles have been retrieved correctly

        # --- NEW CODE FOR STEP 2: Summarize ---

        print("\n🤖 Starting LLM Summarization...")

       

        # Iterate over the fetched articles and get a summary for each

        for item in newsletter_items:

            # Generate the summary and store it

            item['summary'] = summarize_article(item['content_to_summarize'])

       

        # 2. Test by printing the summary of the first article (Required Test)

        print("✅ Summarization Complete. Sample Summary:")

        print(f"Title: {newsletter_items[0]['title']}")

        print(f"Summary:\n{newsletter_items[0]['summary']}")

        print("---------------------------------------")

       

        # ... (The block above this is the working Step 2 logic)



        # The 'newsletter_items' list is now ready for Step 3: Email!



        # --- NEW CODE FOR STEP 3: Send the Email ---

        print("\n✉️ Starting Email Send...")

       

        send_newsletter(

            newsletter_items,

            SENDER_EMAIL,

            SENDER_PASSWORD,

            RECIPIENT_EMAIL,

            SMTP_SERVER,

            SMTP_PORT,

            TOPIC_OF_INTEREST # Passing the topic for the email subject/body

        )

       

    else:

        # This is the single, correct 'else' block

        print("The script cannot proceed without articles.")