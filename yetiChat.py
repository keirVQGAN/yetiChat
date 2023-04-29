import os
import openai
import time
import warnings
import shutil
from google.colab import drive
from IPython.display import clear_output
import requests
import json
from typing import List, Union, Optional, Dict
from pathlib import Path
from rich import print, panel as rich_panel, text as rich_text, console as rich_console

console = rich_console.Console()

def image(title, animal, api_key, prompt, width=512, height=512, samples=2, mask_image=None,
          prompt_strength=None, num_inference_steps=30, guidance_scale=7, enhance_prompt='no', seed=None,
          webhook=None, track_id=None):
    """
    This function generates an image based on the given prompt, and other parameters.
    """

    def clean_filename(text):
        """
        This function cleans up the given text and returns a cleaned up version.
        """
        result = text.replace(' ', '_')
        return result

    negative = '/content/drive/MyDrive/mani/in/txt/negative_prompts.txt'
    with open(negative, 'r') as file:
        negative_prompt = file.read()

    headers = {'Content-Type': 'application/json'}
    output_dir = f'/content/drive/MyDrive/mani/out/manifestos/{title}'
    url = 'https://stablediffusionapi.com/api/v3/text2img'
    data = {
        "key": api_key,
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "width": str(width),
        "height": str(height),
        "samples": str(samples),
        "num_inference_steps": str(num_inference_steps),
        "guidance_scale": guidance_scale,
        "enhance_prompt": enhance_prompt,
        "seed": seed,
        "webhook": webhook,
        "track_id": track_id
    }

    if mask_image:
        data["mask_image"] = mask_image

    if prompt_strength:
        data["prompt_strength"] = prompt_strength

    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response

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

