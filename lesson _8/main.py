import json
import requests
import folium 
import os
from dotenv import load_dotenv 
from geopy import distance
from pprint import pprint

def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json(
    )['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def nearest_coffe(coffeee):
    return coffeee["distancee"]


def main():
    with open("coffee.json", "r", encoding="CP1251") as my_file:
        coffee = my_file.read()


    coffee = json.loads(coffee)
    first_coffee = coffee[0]
    first_coffee_name = coffee[0]["Name"]
    first_coffee_cordinatt = coffee[0]["geoData"]["coordinates"][0]
    first_coffee_cordinattt = coffee[0]["geoData"]["coordinates"][1]
    first_coffee_cordinattt1 = (first_coffee_cordinattt, first_coffee_cordinatt)

    load_dotenv()
    apikey = os.getenv("PASSWORD")
    address = input("Введите местоположение:")


    coords = fetch_coordinates(apikey, address)
    longitude_ya = coords[0]
    latitude_ya = coords[1]
    coords3 = (latitude_ya, longitude_ya)


    first_coffee_namee = {
        "title": first_coffee_name,
        "distancee": distance.distance( first_coffee_cordinattt1,coords3 ).km,
        "latitude": first_coffee_cordinattt,
        "longitude": first_coffee_cordinatt
    }

    coffeee = []


    for i in range(968):
        first_coffee = coffee[i]
        first_coffee_name = coffee[i]["Name"]
        first_coffee_cordinatt = coffee[i]["geoData"]["coordinates"][0]
        first_coffee_cordinattt = coffee[i]["geoData"]["coordinates"][1]
        first_coffee_cordinattt1 = (first_coffee_cordinattt, first_coffee_cordinatt)
        first_coffee_namee[i] = {
            "title": first_coffee_name,
            "distancee": distance.distance( first_coffee_cordinattt1,coords3 ).km,
            "latitude": first_coffee_cordinattt,
            "longitude": first_coffee_cordinatt
        }
        coffeee.append(first_coffee_namee[i],)


    distance1 = sorted(coffeee, key=nearest_coffe)
    top_five = distance1[:5] 


    m = folium.Map(location=(latitude_ya, longitude_ya))
    folium.Marker(
        location=[latitude_ya, longitude_ya],
        tooltip="Я здесь!",
        icon=folium.Icon(color="red"),
    ).add_to(m)


    for i in range(5): 
        folium.Marker(
            location=[top_five[i]["latitude"], top_five[i]["longitude"]],
            tooltip=[top_five[i]["title"]],
            icon=folium.Icon(color="green"),
        ).add_to(m)
    m.save("index.html") 


if __name__ == '__main__':
    main()
