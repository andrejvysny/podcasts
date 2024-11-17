import sys
from search import wide_search
from parse import get_content
from gpt import validate_relevance, search_prompt, analyze_idea, audio_prompt, image_prompt, generate_image
import json

import urllib3

urllib3.disable_warnings()

def relevance(topic, content, url):
    if content:
        print(f"Validating: {url}")
        relevance = validate_relevance(content, topic)
        print(f"Relevance Decision: {relevance}\n\n")
        if "Accept" in relevance:
                return {
                        "url": url,
                        "topic": topic,
                        "content": content,
                        "relevance": relevance
                        }
    return None

    

def find_sources(topic):
  
    search_prompts = search_prompt(topic).replace("- ","").split("\n")

    print(f"Search Prompts: {len(search_prompts)}")
    urls = wide_search(search_prompts)

    print(f"Search Results: {len(urls)}")

    with open("wide_search_results.json", "r") as f:
        urls = json.load(f)

    relevant_sources = []

    for search in urls:

        for google_url in search['google']:
            try:
                print(f"Getting content from {google_url}")
                content = get_content(google_url)
                if not content:
                    print(f"Error getting content from {google_url}")
                    continue
                result = relevance(topic, content, google_url)
                if result:
                    relevant_sources.append(result)
                    print(f"Relevant source added: {google_url}")
            except Exception as e:
                print(f"Error getting content from {google_url}: {e}")

    """
        for scholar_url in search['scholar']:
            try:

                content = get_content(scholar_url)
                result = relevance(topic, content, scholar_url)
                if result:
                    relevant_sources.append(result)
                    print(f"Relevant source found: {scholar_url}")
            except Exception as e:
                print(f"Error getting content from {scholar_url}: {e}")
    """
    with open("relevant_sources.json", "w") as f:
        json.dump(relevant_sources, f, indent=4)
    return relevant_sources
                


if __name__ == "__main__":
    #idea = input("Enter the idea you want to analyze: ")
    idea = """
DNS Explained: The Phonebook of the Internet:
Describe how the Domain Name System (DNS) translates domain names into IP addresses, making it possible for humans to access websites easily. Cover DNS records, caching, and common issues.

        """
    analysis = analyze_idea(idea)
    print(f"\nAnalysis: {analysis}\n\n")
    audio = audio_prompt(analysis)
    print(f"Audio Prompt: {audio}\n\n")

    #imageprompt = image_prompt(idea, analysis)
    #generate_image(imageprompt)
    #generate_image(imageprompt)

    with open("audio_prompt.txt", "w") as f:
        f.write(audio)

    sources = find_sources(analysis)
    print(f"Sources found: {len(sources)}")