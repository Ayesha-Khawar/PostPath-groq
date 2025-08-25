import pandas as pd
import json

class FewShotPosts:
    def __init__(self, file_path="data/posts.json"):
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)

    def load_posts(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            posts = json.load(f)
            # Normalize JSON
            self.df = pd.json_normalize(posts)
            # Collect unique tags
            all_tags = self.df['tags'].apply(lambda x: x).sum()
            self.unique_tags = list(set(all_tags))

    def get_filtered_posts(self, length=None, tag=None):
        df_filtered = self.df
        if tag:
            df_filtered = df_filtered[df_filtered['tags'].apply(lambda tags: tag.lower() in [t.lower() for t in tags])]
        if length:
            df_filtered = df_filtered[df_filtered['length'].str.lower() == length.lower()]
        return df_filtered.to_dict(orient='records')

    def get_tags(self):
        return self.unique_tags

if __name__ == "__main__":
    fs = FewShotPosts()
    posts = fs.get_filtered_posts(length="medium", tag="career")
    print(posts)
