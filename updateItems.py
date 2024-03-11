import requests
import json
import time

def get_item_prefixes(item_id):
    response = requests.get(f"https://api.guildwars2.com/v2/items/{item_id}")
    try:
        item_details = response.json()
        if 'details' in item_details and 'stat_choices' in item_details['details']:
            stat_ids = item_details['details']['stat_choices']
            prefixes = []
            for stat_id in stat_ids:
                stat_response = requests.get(f"https://api.guildwars2.com/v2/itemstats/{stat_id}")
                stat_details = stat_response.json()
                if 'name' in stat_details:
                    prefixes.append(stat_details['name'])
                time.sleep(0.1)  # Add a short delay to avoid hitting rate limits
            return prefixes
    except ValueError:
        print(f"Error parsing JSON for item ID {item_id}. Response status code: {response.status_code}")
    return []

def main():
    with open("items.json", "r") as file:
        data = json.load(file)

    for item in data['items']:
        print(f"Processing item ID {item['id']}...")  # Log progress
        item['prefixes'] = get_item_prefixes(item['id'])

    with open("updated_items.json", "w") as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    main()

