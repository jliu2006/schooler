# google search engine details (cx is the code)
# <script async src="https://cse.google.com/cse.js?cx=73d7fdc99fe7141b9">
# </script>
# <div class="gcse-search"></div>
# api key: AIzaSyBl9WeKsCwckDpgbQ9DoPgYz5fQ3ITXksk
import json
import requests

API_KEY = 'AIzaSyBl9WeKsCwckDpgbQ9DoPgYz5fQ3ITXksk'
CX = '73d7fdc99fe7141b9'

def google_search(query):
    search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CX}"
    response = requests.get(search_url)

    if response.status_code == 200:
        search_results = response.json()
        return search_results
    else:
        print(f"Error: HTTP {response.status_code}")
        try:
            print("Response:", response.json())
        except json.JSONDecodeError:
            print("Failed to parse response as JSON")
        return None

query = "Hope Technology School" + " facebook"
results = google_search(query)

if results:
    # Extract the search results
    search_items = results.get("items", [])
    if not search_items:
        print("No search results found.")
    else:
        search_results = [{"title": item["title"], "link": item["link"]} for item in search_items]

        # Save to JSON
        file_path = "google_search_results.json"
        with open(file_path, "w") as file:
            json.dump(search_results, file, indent=4)

        print("Search results saved to google_search_results.json")
else:
    print("Failed to retrieve search results.")