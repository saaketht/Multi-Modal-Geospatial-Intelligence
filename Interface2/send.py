import replicate

# make function for sending prompt to model and receiving body and sending it


def send_and_receive(prompt, picture, history):
    image = open(picture, "rb")
    answer = replicate.run(
        "yorickvp/llava-v1.6-mistral-7b:19be067b589d0c46689ffa7cc3ff321447a441986a7694c01225973c2eafc874",
        input={
            "image": image,
            "top_p": 1,
            "prompt": prompt,
            "history": history,
            "max_tokens": 1024,
            "temperature": 0.2
        }
    )
    return answer
chat_history = ["User: What is pictured here?",
                        "Agent: The image shows a logo consisting of a stylized basketball with flames coming out of it, set against a black background. The basketball is colored in shades of blue and pink, and the flames are in a gradient of pink to blue. Below the logo, there is text that reads \"MIAMI,\" which is likely the name of the team or organization associated with the logo. The design is reminiscent of the Miami Heat, a professional basketball team based in Miami, Florida. ",
                        "User: What are the most prominent colors?",
                        "Agent: The most prominent colors in the logo are blue, pink, and black. The basketball itself is colored in shades of blue and pink, while the flames are in a gradient of pink to blue. The background is black, which helps the logo stand out. "]

output = send_and_receive("What other color is present?", "uploads/vice.png", chat_history)
# The yorickvp/llava-13b model can stream output as it's running.
# The predict method returns an iterator, and you can iterate over that output.
for item in output:
    # https://replicate.com/yorickvp/llava-13b/api#output-schema
    print(item, end="")
