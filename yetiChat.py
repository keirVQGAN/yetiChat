from typing import List, Union, Optional, Dict
import os, json, openai, datetime, time
from pathlib import Path
from rich import print, panel as rich_panel, text as rich_text, console as rich_console

console = rich_console.Console()

def chatAPI(user: str, system: str, gpt_model: str = "gpt-3.5-turbo", name: Optional[str] = None, temperature: float = 1, top_p: float = 1, n: int = 1, stream: bool = False, stop: Optional[Union[str, List[str]]] = None, max_tokens: Optional[int] = None, presence_penalty: float = 0, frequency_penalty: float = 0, logit_bias: Optional[Dict[int, float]] = None) -> Dict:
    messages = [
        {"role": "user", "content": user},
        {"role": "system", "content": system, "name": name} if name else {"role": "system", "content": system}
    ]

    api_call_args = {
        "model": gpt_model,
        "messages": messages,
        "temperature": temperature,
        "top_p": top_p,
        "n": n,
        "stream": stream,
        "stop": stop,
        "max_tokens": max_tokens,
        "presence_penalty": presence_penalty,
        "frequency_penalty": frequency_penalty
    }
    
    if logit_bias is not None:
        api_call_args["logit_bias"] = logit_bias

    completion = openai.ChatCompletion.create(**api_call_args)
    
    gpt_reply = completion.choices[0].message.content.strip()
    title(gpt_reply)
    return completion.to_dict()

def saveJSON(file_path: str, data: Dict, mode: str = 'w') -> None:
    file_path = Path(file_path)
    
    if file_path.exists():
        with file_path.open('r') as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    if data['id'] not in [entry['id'] for entry in existing_data]:
        existing_data.append(data)
        with file_path.open('w') as f:
            json.dump(existing_data, f, indent=4)
            
def heading(title: Optional[str] = None) -> None:
    console.print(rich_console.Rule(title, style="bright_white"))

def title(title: str, colour: str = "c") -> None:
    title_text = rich_text.Text(title, style="white")
    colour = {"c": "cyan", "m": "magenta", "y": "yellow"}.get(colour, colour)
    console.print(rich_panel.Panel(title_text, expand=False, style=f"{colour} on black"))

def timeTaken(start_time: float) -> None:
    time_taken_float = "%s seconds" % (time.time() - start_time)
    time_taken_split = str(time_taken_float).split('.')
    time_taken_short = time_taken_split[0] + time_taken_split[1][:0]
    title(f'Complete: {time_taken_short} Seconds', "white")
