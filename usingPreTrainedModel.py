import torch
from diffusers import StableDiffusionPipeline

model_id = "CompVis/stable-diffusion-v1-4"
device = "cpu"


pipe = StableDiffusionPipeline.from_pretrained(model_id 
                                               )#, torch_dtype=torch.float16)
pipe = pipe.to(device)

prompt = "a photo of valentina adjimann looking at axel fridman"
image = pipe(prompt).images[0]  
    
image.save("valen_look_axel_pretrained.png")