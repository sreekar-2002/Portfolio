import os
from openai import OpenAI

client = OpenAI()

def generate_project_image(project_description: str) -> str:
    """Generate an image based on project description using DALL-E"""
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"Create a modern, minimalist tech illustration for: {project_description}. Style: Professional, modern, abstract, suitable for a portfolio website",
            size="1024x1024",
            quality="standard",
            n=1,
        )

        # Get the URL of the generated image
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        print(f"Error generating image: {e}")
        return ""  # Return empty string instead of None to match return type