import praw
import openai
import os

# Reddit credentials
reddit = praw.Reddit(
    client_id="your client ID",
    client_secret="your client secret",
    username="Bot's Reddit Username",
    password="Bot's Reddit password",
)

# OpenAI API key
openai.api_key = ""

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

def load_replied_ids(file_name):
    if os.path.isfile(file_name):
        with open(file_name, "r") as f:
            replied_ids = f.read().splitlines()
    else:
        replied_ids = []

    return set(replied_ids)

def save_replied_id(file_name, comment_id):
    with open(file_name, "a") as f:
        f.write(f"{comment_id}\n")

def monitor_and_reply(username, trigger_phrase, replied_ids_file):
    user = reddit.redditor(username)
    replied_ids = load_replied_ids(replied_ids_file)

    for comment in user.stream.comments():
        if comment.id in replied_ids:
            continue

        if trigger_phrase in comment.body and comment.author == username:
            query_start = comment.body.find(trigger_phrase) + len(trigger_phrase)
            query = comment.body[query_start:].strip()
            prompt = f"RADAR-Bot {query}"
            response = ask_chatgpt(prompt)
            comment.reply(response)

            replied_ids.add(comment.id)
            save_replied_id(replied_ids_file, comment.id)

if __name__ == "__main__":
    monitor_and_reply("Reddit User you want to monitor", "Trigger Phase", "replied_ids.txt")
