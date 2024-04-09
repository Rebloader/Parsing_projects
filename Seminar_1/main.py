import requests
import json

client_id = '__'
client_secret = '__'

endpoint = "https://api.foursquare.com/v3/places/search"


def search_places(city, category):
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "near": city,
        "query": category
    }

    headers = {
        "Accept": "application/json",
        "Authorization": "fsq3V3AFHzvqod5PVkb9j5ptfec29VfLTGG2XbHrQEGC8bI="
    }

    try:
        response = requests.get(endpoint, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get('results', [])
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []


def print_places_info(places):
    for place in places:
        name = place.get('name', 'Unknown')
        address = place['location'].get('address', 'Unknown')
        print('Название:', name)
        print('Адрес:', address)
        print('\n')


def main():
    city = input('Введите город: ')
    category = input('Введите категорию: ')
    places = search_places(city, category)
    if places:
        print("Результаты поиска:")
        print_places_info(places)
    else:
        print("Ничего не найдено.")


if __name__ == "__main__":
    main()
