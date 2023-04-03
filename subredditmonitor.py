import praw
import openai

# Reddit credentials
reddit = praw.Reddit(
    client_id="your client ID",
    client_secret="your client secret ID",
    username="Bot's Reddit Username",
    password="Bot's Reddit password",
)

# OpenAI API key
openai.api_key = "Your Open AI API Key"

def ask_chatgpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()

def monitor_and_reply(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)

    for submission in subreddit.stream.submissions():
        prompt = f"{submission.title}\n\n{submission.selftext}"
        response = ask_chatgpt(prompt)
        submission.reply(response)

if __name__ == "__main__":
    monitor_and_reply("Name of your Subreddit")
