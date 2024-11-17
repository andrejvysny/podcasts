import json

# Load the JSON file
with open('relevant_sources.json', 'r') as file:
    data = json.load(file)

# Extract URLs
urls = [source['url'] for source in data if 'url' in source]


# Write URLs to a text file, each on a new line
with open('urls.txt', 'w') as file:
    for url in urls:
        file.write(url + '\n')