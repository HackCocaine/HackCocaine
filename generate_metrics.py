import json
import os
from pathlib import Path

from diffusers import StableDiffusionPipeline

stars = os.environ.get("STARS", "0")
forks = os.environ.get("FORKS", "0")
issues = os.environ.get("ISSUES", "0")

prompts = [
    f"Minimalist neon particle style, glowing lines and dots, representing {stars} stars on GitHub",
    f"Clean futuristic neon visual for {forks} forks with subtle particle glow",
    f"Soft glowing particle graph representing {issues} open issues, minimalistic",
]

Path("assets").mkdir(exist_ok=True)

pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipe.enable_attention_slicing()

for i, prompt in enumerate(prompts):
    img = pipe(prompt, height=400, width=800, num_inference_steps=20).images[0]
    img.save(f"assets/metric_{i + 1}.png")

with open("prompts.json", "w") as f:
    json.dump(prompts, f)
