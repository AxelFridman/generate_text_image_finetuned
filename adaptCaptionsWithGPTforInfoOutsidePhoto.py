import json
from openai import OpenAI
import os

client = OpenAI(api_key='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')

general_message = """
Objective: Your task is to generate three unique captions based on an original caption provided for an image. The enhancement required is the explicit identification of the individuals in the photos when the original caption falls short. Specifically, when the photo includes individuals, you must recognize Valentina Adjimann and Axel Fridman by name.

Context: The original captions might generically refer to people in the image, such as "a couple" or "a person." It's crucial to adjust these captions to specifically mention "Valentina Adjimann" (also referred to as "Valen") when she is alone in the photo or "Valentina and Axel" when they appear together. This explicit naming adds a personal touch and accuracy to the captions.

Output Format: Please present your revised captions in a Python list format, ensuring that each caption is distinct yet retains the informational essence of the original. The goal is to use varied wording to maintain interest and engagement.
"""
captionOriginalEjemplo1 = 'A couple in a park with roses.'
respuestaEjemplo1 = '["Valentina and Axel enjoying a serene stroll among the roses", "Valen and Axel, surrounded by the vibrant hues of rose blossoms", "In a garden of roses, Valentina Adjimann and Axel Fridman share a moment of togetherness"]'

captionOriginalEjemplo2 = 'A person running with a yellow dress.'
respuestaEjemplo2 = '["Valentina Adjimann training in a striking yellow dress", "Valentina dashing through the scenery in her vibrant yellow attire","With grace and speed, Valen makes the park her runway in a yellow dress"]'

def generateResponse(caption):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": general_message},
        {"role": "user", "content": captionOriginalEjemplo1},
        {"role": "assistant", "content": respuestaEjemplo1},
        {"role": "user", "content": captionOriginalEjemplo2},
        {"role": "assistant", "content": respuestaEjemplo2},
        {"role": "user", "content": caption}
    ]
    )
    return (response.choices[0].message.content)


with open(os.path.join(os.getcwd(), 'captiones_with_gpt.json'), 'r') as json_file:
    dic = json.load(json_file)


for photo in dic["photos"]:
    if "gptResponse" not in photo:
        try:
            print("Processing photo: ", photo["name"])
            print(photo["caption"])
            #photo["caption"] = photo["caption"][0]
            caption = photo["caption"]

            res = generateResponse(caption)
            captions_list = json.loads(res)

            photo["gptResponse"] = captions_list
            photo["captionGpt1"] = captions_list[0]
            photo["captionGpt2"] = captions_list[1]
            photo["captionGpt3"] = captions_list[2]
            
            with open(os.path.join(os.getcwd(), 'captiones_with_gpt.json'), 'w') as json_file:
                json.dump(dic, json_file)

        except:
            print()
            print("Error with photo: ", photo["name"])
            print()

#res = generateResponse('A person showing off her arms.')
#print(res)




