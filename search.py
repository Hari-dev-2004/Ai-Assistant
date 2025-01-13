import requests
from speech import speak

DUCKDUCKGO_API_URL = "https://api.duckduckgo.com/"

def perform_web_search(query):
    search_query = query.split("search", 1)[1].strip()
    
    # Making the API request to DuckDuckGo Instant Answer API
    params = {
        "q": search_query,
        "format": "json",
        "no_html": 1,  # Exclude HTML content
        "skip_disambig": 1  # Avoid ambiguous answers
    }
    
    response = requests.get(DUCKDUCKGO_API_URL, params=params)
    
    if response.status_code == 200:
        results = response.json()
        
        # Parsing and speaking the search results
        if "RelatedTopics" in results and results["RelatedTopics"]:
            for idx, result in enumerate(results["RelatedTopics"][:3]):  # Get top 3 results
                title = result.get("Text", "No title")
                link = result.get("FirstURL", "#")
                snippet = result.get("Result", "No description available.")
                
                summary = f"Result {idx+1}: {title}\nLink: {link}\nSummary: {snippet}\n"
                print(summary)
                
                # Speak out the summary
                speak(f"Result {idx+1}: {title}. Link: {link}. Summary: {snippet}")
        else:
            speak("Sorry, I couldn't find any relevant search results.")
    else:
        speak("Sorry, there was an error while searching the web.")
