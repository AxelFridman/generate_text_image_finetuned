from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
from PIL import Image
import os
import json

model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)



max_length = 16
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}
def predict_step(image_paths):
  images = []
  for image_path in image_paths:
    i_image = Image.open(image_path)
    if i_image.mode != "RGB":
      i_image = i_image.convert(mode="RGB")

    images.append(i_image)

  pixel_values = feature_extractor(images=images, return_tensors="pt").pixel_values
  pixel_values = pixel_values.to(device)

  output_ids = model.generate(pixel_values, **gen_kwargs)

  preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
  preds = [pred.strip() for pred in preds]
  return preds

lista1 = os.listdir('/Users/imac/Downloads/valentinaPhotos')
lista = [img for img in lista1 if (('png' in img) or ('jpg' in img))]
granjson = {}
granjson["photos"] = []
for i in lista:
  thisPic = {}
  thisPic["name"] = i
  thisPic["caption"] = predict_step(['/Users/imac/Downloads/valentinaPhotos/'+i])
  granjson["photos"].append(thisPic)
  #save as json the dictonary granjson in directory where file is running
  
  with open(os.getcwd() + 'valentinaCaptions.json', 'w') as json_file:
    json.dump(granjson, json_file)
