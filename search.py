from googlesearch import search
import requests
from scholarly import scholarly
import json


def search_bing(query):
    headers = {"Ocp-Apim-Subscription-Key": "YOUR_BING_API_KEY"}
    params = {"q": query, "count": 10}
    response = requests.get("https://api.bing.microsoft.com/v7.0/search", headers=headers, params=params)
    return response.json()


def get_google_results(query, num_results=10):
    """
    Perform a Google search using the googlesearch-python library.
    """
    return [url for url in search(query, num_results=num_results, lang='en', ssl_verify=False, advanced=False)]

def get_scholar_results(query):
    search_query = scholarly.search_pubs(query)
    results = []
    for i in range(10):
        try:
            pub = next(search_query)
            results.append(pub.get('pub_url', ''))
        except StopIteration:
            break
    return results


def wide_search(search_prompts):

    urls=[]
    for prompt in search_prompts:
        try:
            scholar = [] #get_scholar_results(prompt)
            #print(f"Error during scholar search: {e}")
            google = get_google_results(prompt)
            urls.append(
                {
                    "prompt": prompt,
                    "scholar": scholar,
                    "google": google
                }
            )
            print(f"Search prompt: {prompt}, urls found: {len(scholar) + len(google)}")
        except Exception as e:
            print(f"Error during search: {e}")
    with open("wide_search_results.json", "w") as f:
        json.dump(urls, f, indent=4)

    return urls
