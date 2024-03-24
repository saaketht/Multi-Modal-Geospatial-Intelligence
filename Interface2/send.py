import replicate

# make function for sending prompt to model and receiving body and sending it


def sendAndReceive(prompt, picture):
    image = open(picture, "rb")
    answer = replicate.run(
        "yorickvp/llava-13b:a0fdc44e4f2e1f20f2bb4e27846899953ac8e66c5886c5878fa1d6b73ce009e5",
        input={
            # "image": "https://replicate.delivery/pbxt/KRULC43USWlEx4ZNkXltJqvYaHpEx2uJ4IyUQPRPwYb8SzPf/view.jpg",
            "image": image,
            "top_p": 1,
            "prompt": prompt,
            "max_tokens": 1024,
            "temperature": 0.2
        }
    )
    return answer


output = sendAndReceive("What is pictured here?", "uploads/vice.png")
# output = replicate.run(
#     "yorickvp/llava-13b:a0fdc44e4f2e1f20f2bb4e27846899953ac8e66c5886c5878fa1d6b73ce009e5",
#     input={
#         "image": "https://replicate.delivery/pbxt/KRULC43USWlEx4ZNkXltJqvYaHpEx2uJ4IyUQPRPwYb8SzPf/view.jpg",
#         "top_p": 1,
#         "prompt": "Are you allowed to swim here?",
#         "max_tokens": 1024,
#         "temperature": 0.2
#     }
# )

instructions = {}

# The yorickvp/llava-13b model can stream output as it's running.
# The predict method returns an iterator, and you can iterate over that output.
for item in output:
    # https://replicate.com/yorickvp/llava-13b/api#output-schema
    print(item, end="")
