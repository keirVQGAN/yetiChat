import os, json, openai, datetime
from rich import print
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
console = Console()

def chatAPI(USER, SYSTEM, GPT_MODEL="gpt-3.5-turbo"):
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

def title(title,colour="c"):
    title_text = Text(title, style="white")
    if colour == "c": colour = "cyan"
    if colour == "m": colour = "magenta"
    if colour == "y": colour = "yellow"
    
    console.print(Panel(title_text, expand=False, style=f"{colour} on black"))

def timeTaken(start_time):
    import time
    timeTakenFloat = "%s seconds" % (time.time ( ) - start_time)
    timeTaken = timeTakenFloat
    timeTaken_str = str ( timeTaken )
    timeTaken_split = timeTaken_str.split ( '.' )
    timeTakenShort = timeTaken_split [ 0 ] + '' + timeTaken_split [ 1 ] [ :0 ]
    title ( f'Complete: {timeTakenShort} Seconds', "Bright White")
