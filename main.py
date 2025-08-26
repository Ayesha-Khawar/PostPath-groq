import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post
from PIL import Image

# Options for length
length_options = ["Short", "Medium", "Long"]

# Main app layout
def main():
    st.set_page_config(page_title="PostPath", layout="wide")
    st.title("PostPath - Guided Post Generator")
    st.markdown("""
        Generate posts based on topic, author style, and additional context.
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

    st.markdown("### Optional Image")
    uploaded_image = st.file_uploader("Upload an image for the post (optional)", type=["png", "jpg", "jpeg"])
    image_caption = ""
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        # Here, you can implement image captioning if you want, for now we just note that an image is included
        image_caption = "The post should include content inspired by the uploaded image."

    st.markdown("---")

    # Generate button centered
    if st.button("Generate Post"):
        with st.spinner("Generating post..."):
            post = generate_post(selected_length, selected_author, selected_tag, context=additional_context, image_context=image_caption)

        # Display generated post
        st.markdown("### Generated Post")
        st.code(post, language="markdown")


if __name__ == "__main__":
    main()
