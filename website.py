import webbrowser

def open_website(query):
    if "youtube" in query:
        if "search for" in query:
            search_query = query.split("search for", 1)[1].strip()
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        else:
            webbrowser.open("https://www.youtube.com")
    elif "wikipedia" in query:
        if "search for" in query:
            search_query = query.split("search for", 1)[1].strip()
            webbrowser.open(f"https://en.wikipedia.org/wiki/{search_query}")
        else:
            webbrowser.open("https://www.wikipedia.org")
    elif "amazon" in query:
        if "search for" in query:
            search_query = query.split("search for", 1)[1].strip()
            webbrowser.open(f"https://www.amazon.com/s?k={search_query}")
        else:
            webbrowser.open("https://www.amazon.com")
    elif "google" in query:
        webbrowser.open("https://www.google.com")
    elif "reddit" in query:
        webbrowser.open("https://www.reddit.com")
    elif "facebook" in query:
        webbrowser.open("https://www.facebook.com")
    elif "twitter" in query:
        webbrowser.open("https://www.twitter.com")
    elif "instagram" in query:
        webbrowser.open("https://www.instagram.com")
    elif "linkedin" in query:
        webbrowser.open("https://www.linkedin.com")
    elif "github" in query:
        webbrowser.open("https://www.github.com")
    elif "twitch" in query:
        webbrowser.open("https://www.twitch.tv")
    elif "netflix" in query:
        webbrowser.open("https://www.netflix.com")
    elif "spotify" in query:
        webbrowser.open("https://www.spotify.com")
    elif "yahoo" in query:
        webbrowser.open("https://www.yahoo.com")
    elif "bing" in query:
        webbrowser.open("https://www.bing.com")
    elif "quora" in query:
        webbrowser.open("https://www.quora.com")
    else:
        print("Website not recognized or not supported for search.")
