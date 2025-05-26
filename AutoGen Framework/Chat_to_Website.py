# Talk_to_Website
# This script creates a simple chatbot that extracts text from a given website, and you can ask questions about the content of that website.
import requests
from bs4 import BeautifulSoup
import re
import getpass
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import SseMcpToolAdapter, SseServerParams
import asyncio 

# Function to extract text from a website
def extract_text_from_website(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract headline (title tag)
        headline = soup.title.string.strip() if soup.title and soup.title.string else ""

        # Extract meta description
        meta_desc = ""
        meta = soup.find('meta', attrs={'name': 'description'})
        if meta and meta.get('content'):
            meta_desc = meta['content'].strip()

        # Extract headings (h1, h2, h3)
        headings = []
        for tag in ['h1', 'h2', 'h3']:
            headings.extend([h.get_text(strip=True) for h in soup.find_all(tag)])

        # Extract paragraphs
        paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]

        # Combine all extracted parts
        website_text = "\n".join([
            f"Headline: {headline}" if headline else "",
            f"Meta Description: {meta_desc}" if meta_desc else "",
            "Headings: " + "; ".join(headings) if headings else "",
            "Content: " + " ".join(paragraphs) if paragraphs else ""
        ]).strip()
    except Exception as e:
        return f"Error reading website: {e}"
    return website_text

# Function to preprocess the text
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = re.sub(r'[^\w\s]', '', text)  # Remove non-alphanumeric characters except spaces
    return text

# Function to answer questions using OpenAI API
async def answer_question(api_key, question, context):
    try:
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", api_key=api_key)

        # Define an AssistantAgent with the model, tool, system message.
        agent = AssistantAgent(
            name="website_agent",
            model_client=model_client,
            system_message=f"You are a helpful assistant and this is the context: {context}"     
            )

        # Run the agent and await the response
        response = await agent.run(task=f"Question: {question}")
        return response.messages[-1].content # Return the last message content as the answer

    except Exception as e:
        print(f"Error with AssistantAgent: {e}")
        return None

async def main():
    print("Welcome to the Chat with Website!")

    # Get OpenAI API key
    api_key = getpass.getpass("Enter your OpenAI API Key: ").strip()
    if not api_key:
        print("Error: API key is required.")
        return

    # Load and preprocess text
    preprocessed_text = ""
    url = input("Enter the website URL (leave blank to chat directly with LLM): ").strip()
    if url:
        print("Extracting text from the website...")
        website_text = extract_text_from_website(url)
        if "Error" in website_text:
            print(website_text)
            return
        preprocessed_text = preprocess_text(website_text)
        print("Website text extracted and preprocessed.")
    else:
        print("No URL provided. You can chat directly with the LLM.")

    # Question and answer loop
    while True:
        question = input("\nEnter your question (or type 'exit' to quit): ").strip()
        if question.lower() == 'exit':
            print("Goodbye!")
            break
        if not question:
            print("Error: Question cannot be empty.")
            continue
        print("Fetching answer...")
        answer = await answer_question(api_key, question, preprocessed_text)
        print(f"Answer: {answer}")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")

