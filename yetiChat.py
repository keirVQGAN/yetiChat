import os, json, openai, datetime
from rich import print
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
console = Console()

def mount():
  if not os.path.isdir('/content/drive'):
    from google.colab import drive
    drive.mount('/content/drive')

def chatAPI(USER, SYSTEM, GPT_MODEL):
    completion = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=[
            {"role": "user", "content": USER},
            {"role": "system", "content": SYSTEM}
        ]
    )
    GPT_REPLY = completion.choices[0].message.content.strip()
    print(GPT_REPLY) 
    return completion.to_dict()

def saveJSON(file_path, data, mode='w'):
    existing_data = []

    # Load existing data
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            existing_data = json.load(f)

    # Check if the new entry is not a duplicate
    entry_id = data['id']
    if entry_id not in [entry['id'] for entry in existing_data]:
        existing_data.append(data)
        with open(file_path, 'w') as f:
            json.dump(existing_data, f, indent=4)
        print(f'Saved data to {file_path}')
    else:
        print(f'Data with id {entry_id} already exists in {file_path}')

def heading(title=None):
    console.print(Rule(title, style="bright_white"))

def title(title,colour):

if __name__ == '__main__':
