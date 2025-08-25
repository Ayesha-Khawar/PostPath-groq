import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post

# Options for length
length_options = ["Short", "Medium", "Long"]

# Main app layout
def main():
    st.set_page_config(page_title="PostPath", layout="wide")
    st.title("PostPath - Guided Post Generator")
    st.markdown("""
        Generate LinkedIn posts based on topic, author style, and additional context.
        Provide extra details to guide the tone, situations, or audience for the post.
    """)

    # Initialize few-shot data
    fs = FewShotPosts()
    tags = fs.get_tags()
    authors = list(fs.df['author'].unique())

    # Filter selections in columns
    with st.container():
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            selected_tag = st.selectbox("Topic", options=tags)
        with col2:
            selected_length = st.selectbox("Length", options=length_options)
        with col3:
            selected_author = st.selectbox("Author", options=authors)

    st.markdown("### Additional Context")
    additional_context = st.text_area(
        "Provide any extra details, situations, or audience information to guide the post generation.",
        height=120
    )

    st.markdown("---")

    # Generate button centered
    if st.button("Generate Post"):
        with st.spinner("Generating post..."):
            post = generate_post(selected_length, selected_author, selected_tag, context=additional_context)

        # Display generated post
        st.markdown("### Generated Post")
        st.code(post, language="markdown")


if __name__ == "__main__":
    main()
