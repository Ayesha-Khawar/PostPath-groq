import json
from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

def unify_tags_llm(input_file, output_file):
    # Load existing posts
    with open(input_file, encoding='utf-8') as f:
        posts = json.load(f)

    # Collect unique tags
    unique_tags = set()
    for post in posts:
        unique_tags.update(post.get('tags', []))
    unique_tags_list = ', '.join(unique_tags)  # simple string

    # Prompt template — force JSON output
    template = '''You are given a list of tags separated by commas.
Your task is to unify similar tags according to the following rules:
1. Merge similar tags (e.g., "Jobseekers" + "Job Hunting" → "Job Search").
2. Standardize all tags to Title Case.
3. Return a JSON object mapping original tags to unified tags.
4. ONLY RETURN THE JSON OBJECT. NO EXPLANATION.

Tags: {{tags}}
'''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"tags": unique_tags_list})

    # Parse LLM output as JSON
    try:
        parser = JsonOutputParser()
        unified_mapping = parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException(
            "Failed to parse LLM output. Make sure the model returns JSON only."
        )

    # Apply unified tags to each post
    for post in posts:
        post_tags = post.get('tags', [])
        post['tags'] = [unified_mapping.get(tag, tag) for tag in post_tags]

    # Save output
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=4)
    print(f"Processed posts saved to {output_file}")


if __name__ == "__main__":
    unify_tags_llm("data/posts.json", "data/processed_posts.json")
