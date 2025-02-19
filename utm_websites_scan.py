import requests
import re
import os
import json
from bs4 import BeautifulSoup

def get_utm_subdomains():
    """Fetch subdomains using a predefined list as a fallback."""
    url = "https://crt.sh/?q=%25.utm.my&output=json"
    subdomains = set()
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            try:
                data = response.json()
                for entry in data:
                    subdomains.add(entry['name_value'])
            except json.JSONDecodeError:
                print("Error decoding JSON response from crt.sh")
    except requests.exceptions.RequestException:
        print("Connection error while accessing crt.sh. Using fallback list.")
        subdomains = {
            "www.utm.my", "fs.utm.my", "library.utm.my", "computing.utm.my",
            "research.utm.my", "student.utm.my", "elearning.utm.my"
        }
    
    return sorted(subdomains)

def categorize_websites(subdomains):
    """Categorize subdomains based on relevance to ChatUTM."""
    categories = {"Relevant": [], "Irrelevant": [], "Unknown": []}
    
    for subdomain in subdomains:
        try:
            response = requests.get(f"http://{subdomain}", timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.title.string if soup.title else ""
                content = soup.get_text().lower()
                
                # Define relevance criteria
                if "chatutm" in content or "student portal" in title.lower():
                    categories["Relevant"].append(subdomain)
                else:
                    categories["Irrelevant"].append(subdomain)
            else:
                categories["Unknown"].append(subdomain)
        except requests.exceptions.RequestException:
            categories["Unknown"].append(subdomain)
    
    return categories

def save_to_file(categories, directory="/sources"):
    """Save categorized subdomains to a text file."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    filepath = os.path.join(directory, "websites_list.txt")
    with open(filepath, "w") as f:
        for category, sites in categories.items():
            f.write(f"{category} Websites:\n")
            for site in sites:
                f.write(f"- {site}\n")
            f.write("\n")

def main():
    subdomains = get_utm_subdomains()
    if not subdomains:
        print("No subdomains found. Exiting...")
        return
    
    categories = categorize_websites(subdomains)
    save_to_file(categories)
    print("Task completed. Websites saved in /sources/websites_list.txt")

if __name__ == "__main__":
    main()
