from llm_helper import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()

def generate_post(length, author, tag, context=""):
    prompt = get_prompt(length, author, tag, context)
    response = llm.invoke(prompt)
    return response.content


def get_prompt(length, author, tag, context=""):
    prompt = f"""
Generate a LinkedIn post using the below information. No preamble. Avoid Emoji.

1) Topic: {tag}
2) Length: {length}
3) Author: {author}
The script for the generated post should always be in English. Follow the writing style of the author, but do NOT include their name in the post.
"""

    if context:
        prompt += f"\n4) Include this context/situation in the post: {context}"

    # Fetch few-shot examples
    examples = few_shot.get_filtered_posts(length=length, tag=tag)
    examples = [post for post in examples if post['author'].lower() == author.lower()]

    if examples:
        prompt += "\n5) Use the writing style as per the following examples:"

    for i, post in enumerate(examples):
        post_text = post['content']
        prompt += f"\n\nExample {i+1}:\n{post_text}"
        if i == 2:  # max 3 examples
            break

    return prompt


if __name__ == "__main__":
    print(generate_post("long", "Aleena Shahid", "marketing", "i want people to understand their audience"))
    print(get_prompt("long", "Aleena Shahid", "marketing", "i want people to understand their audience"  ))