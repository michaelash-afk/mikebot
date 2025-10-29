import streamlit as st
import openai

# Set up the page
st.set_page_config(page_title="AI Image Generator 🤖", page_icon="🎨")

# Title and description
st.title("🎨 My AI Image Generator")
st.write("Hello! I’m an AI image generator. Describe an image, and I’ll create it for you!")

# --- Get the OpenAI API key from Streamlit secrets ---
api_key = st.secrets["OPENAI_API_KEY"]

# Set the OpenAI API key
openai.api_key = api_key

# --- Keep chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Show old messages ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat input ---
if prompt := st.chat_input("Describe the image you want to generate..."):
    # Add your message (user's description of the image)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Show user input
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI image generation (call OpenAI's DALL·E API)
    with st.chat_message("assistant"):
        with st.spinner("Generating your image..."):
            try:
                # Request image generation from OpenAI's DALL·E model
                response = openai.Image.create(
                    prompt=prompt,  # the description of the image
                    n=1,             # generate 1 image
                    size="1024x1024" # set image size
                )
                image_url = response['data'][0]['url']  # Extract the image URL from the response
                st.image(image_url, caption="Here is your generated image!", use_container_width=True)

            except Exception as e:
                st.error(f"Error generating image: {str(e)}")

    # Save the reply (in this case, the image URL or success message)
    st.session_state.messages.append({"role": "assistant", "content": "Image generated successfully!"})

