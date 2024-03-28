import replicate
from replicate.client import Client
import os

# Get the API token from the environment variable

api_token = os.environ.get('REPLICATE_API_TOKEN')


def send_and_receive(prompt, image_path, history_dict, top_p=1, max_tokens=1024, temperature=0.2):
    replicate = Client(api_token="r8_OhKVhZSEDFvW9cDHy2kfORWz2AETFgL1axyKl")
    image = open(image_path, "rb")
    output = replicate.run(
        "yorickvp/llava-v1.6-vicuna-13b:0603dec596080fa084e26f0ae6d605fc5788ed2b1a0358cd25010619487eae63",
        input={
            "image": image,
            "top_p": top_p,
            "prompt": prompt,
            "history": history_dict,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
    )
    print(output)
    return output
