from openai import OpenAI
import os
from dotenv import load_dotenv
import requests
load_dotenv()
import time

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

def validate_relevance(content, topic):

    prompt = f"""
Evaluate the relevance of the following content to the topic "{topic}" using these criteria:

Relevance to Topic (0-30 points): The content addresses the topic and provides useful, pertinent information.
Content Quality (0-30 points): The content is informative, accurate, and provides sufficient detail.
Clarity and Structure (0-20 points): The content is well-organized, easy to understand, and logically presented.
Currency of Information (0-20 points): The information is up-to-date or still relevant despite its age.
Instructions:

Ignore any HTML tags, ads, navigation menus, footers, and references to other websites.
Focus solely on the main textual content relevant to the topic.
Do not penalize for minor inaccuracies or older content if it still provides valuable information on the topic.
After evaluating, calculate the total score (out of 100).

Output format (strictly adhere to this):

If the total score is 70 or above, output: Accept:<score>
If the total score is below 70, output: Reject:<score>
Do not include explanations, justifications, or any additional text.

Content to evaluate:

{content}
    """

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are helping to validate the relevance of content for specific topic."},
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return completion.choices[0].message.content.replace("\"", "")
    
    except Exception as e:
        print(f"Error during GPT-4 validation: {e}")
        return "Reject"


def search_prompt(topic):
    system = f"""
        Act as a research assistant, your task is to:
        
        Analyze the given topic or content and identify the most relevant keywords and phrases.

        Generate a bullet list of search prompts to optimize Google search results:
         - Each prompt should focus on key aspects of the topic.
         - Avoid unnecessary text; provide only the search prompts.
         - Ensure the prompts are targeted and specific, enhancing the chances of finding high-quality articles or resources.

        Output: Strictly respond with a bullet list of search prompts.
    """

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system},
                {
                    "role": "user",
                    "content": topic
                }
            ]
        )
        return completion.choices[0].message.content
    
    except Exception as e:
        print(f"Error during GPT-4 search prompt: {e}")
        return ""
    
def image_prompt(idea,content):
    system = f"""
Create a prompt for DALL-E to generate an image focused on the given topic and the detailed content provided through bullet points. Ensure the image is both highly representative and illustrative of the concept provided. The bullet points may include specific descriptions or details that should be incorporated into the image concept. The artistic style of the image will be listed separately.

# Steps

1. **Analyze Topic and Bullet Points**: Break down the given topic along with the additional bullet points detailing the content. Identify any specific imagery or descriptions that need to be visually represented.

2. **Determine Key Symbols or Relevant Imagery**: Identify symbols or iconic elements that are strongly associated with both the topic and any details from the bullet points.

3. **Combine Elements to Create a Coherent Visual Concept**: Integrate the identified symbols and ornate descriptions into a cohesive visual idea, ensuring the resulting prompt conveys a clear scene that would represent the essence of the topic and bullet points.

4. **Express Relationships Between Elements**: Describe how the elements should relate to each other within the image, positioning and aligning them to ensure that the concept is visually intuitive and easy to interpret.

# Output Format

A one-sentence prompt clearly describing the content of the image as it relates to the given topic and each bullet point, incorporating the primary imagery cohesively. The prompt should include specific elements from both the topic and bullet points, making it easy for DALL-E to produce an on-topic image.

# Example

**Input:**
- **Topic**: Docker Containers
- **Content Bullet Points**:
  - A large whale as a central figure
  - Multiple color-coded cargo containers being carried by the whale

**Output:**
“Generate an image featuring a large blue whale carrying several color-coded cargo containers on its back, symbolizing the concept of Docker Containers.”

**Input:**
- **Topic**: Quantum Computing
- **Content Bullet Points**:
  - Several glowing orbs representing qubits
  - The orbs are interconnected with light lines, demonstrating quantum entanglement

**Output:**
“Create an illustration showing interconnected qubits represented as glowing orbs, entangled in a web of light lines, capturing the concept of quantum entanglement in computing.”

# Notes

- **Avoid Mentioning Style**: Only focus on the content of the image. Style considerations will be given separately.
- **Specific Symbols**: Always prioritize symbols and central visual motifs strongly related to the topic and the bullet points given.
- **Clarity & Representation**: Ensure that all elements collectively represent a coherent and descriptive idea of the topic and content, making it easy for DALL-E to visualize accurately.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": f"{idea}\n\n{content}"}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error during GPT-4 audio prompt: {e}")
        return ""

def audio_prompt(content):
    system = f"""
    Generate a prompt for an audio summary of a NotebookLM podcast. 

The prompt should guide podcasters on key topics to focus on based on the provided topic and content. Ensure the following requirements are met:

- Do not include any specific code or special characters.
- Maintain an educational and conversational tone to support learning.
- Keep the prompt succinct, including only important information.

# Output Format

- Maximum of 400 characters.
- Plain text only, with no Markdown formatting.
- Bullet points.
# Notes

- Be concise and relevant to enhance focus on the given topic. 
- Avoid unnecessary details or extended explanations.
"""
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": content}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error during GPT-4 audio prompt: {e}")
        return ""

def analyze_idea(idea):
    system = f"""
As an IT specialist and podcast assistant, your role is to:

Analyze the given topic with a high level of expertise and identify key areas of interest.

Generate podcast content that is engaging and informative:

- The content should be structured logically to enhance listener understanding.
- Provide a mix of high-level concepts and practical insights.
- Avoid complex technical jargon unless it's critical, explaining it simply if used.

List key focus points with a brief one or two-sentence description for each:

- Emphasize essential details or unique aspects of the topic.
- Highlight any contrasts, use cases, or examples where helpful.
- Maintain an educational tone that is clear, concise, and approachable to a broad audience.

Approach every topic as though you are a specialist with extensive experience in IT, ready to guide the user in creating engaging content. 

# Output Format

- Key focus points with brief descriptions (bullet points preferred). 
- Do not include the episode title, topic, introduction, or conclusion. Only list the essential content for the podcast as requested.
"""
    

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": idea}
            ]
        )
        return completion.choices[0].message.content
    
    except Exception as e:
        print(f"Error during GPT-4 search prompt: {e}")
        return ""
    

def generate_image(content):

    prompt = f"""
Generate image for podcast cover according to this specs

Style: 
 - The image should be vector-based and isometric, with a sense of depth while keeping clarity and simplicity. Use a dark, muted color palette featuring shades of blue, green, and teal for a futuristic, high-tech atmosphere. 
 - The colors should be cool and minimal, giving a modern, Matrix-inspired vibe. The illustration should be minimalist yet detailed, with clean lines and sharp edges for a polished, technical feel. Emphasize a digital, sci-fi mood using geometric forms and glowing accents to suggest data flow and tech sophistication.
 - Use a dark background to highlight brighter foreground elements, creating a holographic effect. The overall style should feel precise and technical, suitable for themes of IT, technology, and infrastructure.

Image content: {content}
    """
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url

    image_data = requests.get(image_url).content
    with open(f"podcast_cover_{time.time()}.png", "wb") as handler:
        handler.write(image_data)
    return image_url