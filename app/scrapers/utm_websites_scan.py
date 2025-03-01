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
                print("Subdomains retrieved from crt.sh successfully.")
            except json.JSONDecodeError:
                print("Error decoding JSON response from crt.sh")
    except requests.exceptions.RequestException:
        print("Connection error while accessing crt.sh.")
    
    if not subdomains:
        print("Using predefined fallback list of UTM subdomains.")
        subdomains = {
            "www.utm.my", "fs.utm.my", "library.utm.my", "computing.utm.my",
            "research.utm.my", "student.utm.my", "elearning.utm.my"
        }
    
    if not subdomains:
        print("Error: No subdomains found even in the fallback list.")
    else:
        print(f"Total subdomains retrieved: {len(subdomains)}")
    
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

def save_to_file(categories, directory="./ChatUTM/sources"):
    """Save categorized subdomains to a text file in a Windows-compatible directory and print content."""
    absolute_directory = os.path.abspath(directory)
    if not os.path.exists(absolute_directory):
        os.makedirs(absolute_directory)
    
    filepath = os.path.join(absolute_directory, "websites_list.txt")
    print(f"Saving file at: {filepath}")
    
    try:
        with open(filepath, "w") as f:
            for category, sites in categories.items():
                f.write(f"{category} Websites:\n")
                print(f"\n{category} Websites:")
                for site in sites:
                    f.write(f"- {site}\n")
                    print(f"- {site}")
                f.write("\n")
        
        if os.path.exists(filepath):
            print(f"File successfully saved at: {filepath}")
        else:
            print("Error: File was not created!")
    except Exception as e:
        print(f"Error while saving file: {e}")

def main():
    subdomains = get_utm_subdomains()
    
    if not subdomains:
        print("Critical error: No subdomains found at all. Exiting...")
        return
    
    print(f"Total subdomains to process: {len(subdomains)}")
    categories = categorize_websites(subdomains)
    save_to_file(categories)
    print("Task completed. Check the file location printed above.")

if __name__ == "__main__":
    main()
