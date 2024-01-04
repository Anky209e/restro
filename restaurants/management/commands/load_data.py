from typing import Any
from django.core.management.base import BaseCommand,CommandParser
from dishes.models import Dish
from restaurants.models import Restaurant
import json
import argparse
import csv


class Command(BaseCommand):
    help = "Loads Restaurant Data from csv."

    def add_arguments(self, parser:CommandParser):
        return parser.add_argument("file_path",type=argparse.FileType("r"),help="Data File Path")
    
    def get_dish(self,name:str,price_tag:str,restaurant:Restaurant):
        """
        Returns a Dish Instance with filled information
        """
        price_st = price_tag.split()
        price = float(price_st[0])
        onwards = len(price_st) > 1

        return Dish(
            name = name,
            onwards = onwards,
            price = price,
            restaurant=restaurant,
        )

    def handle(self, *args: Any, **options: Any) -> str | None:
        # Reading CSV file using python csv reader
        csv_reader = csv.reader(options["file_path"])
        # Iterating over first row which contains titles or keys
        next(csv_reader)

        total_res = 0
        total_dish = 0

        for data in csv_reader:
            id,name,location,all_items,cords,details = data

            lat,long = tuple(map(float,cords.split(",")))

            all_items = json.loads(all_items)

            if details:
                details = json.loads(details)
            # If there is no detail
            else:
                details = {
                    "is_delivering_now": 0,
                    "location": {"address": ""},
                    "user_rating": {"aggregate_rating": None},
                }
            
            rating = details["user_rating"]["aggregate_rating"]
            rating = float(rating) if rating else None
            address = details["location"]["address"]
            delivering_now = bool(details["is_delivering_now"])
            

            restaurant = Restaurant.objects.create(
                name=name,
                restro_id=int(id),
                latitude = lat,
                longitude = long,
                address=address,
                rating=rating,
                delivering_now=delivering_now,
            )

            dishes = [
                        self.get_dish(dish_name,price_tag,restaurant) 
                        for dish_name,price_tag in all_items.items()
                    ]
            
            # Adding data to db using Dish model
            Dish.objects.bulk_create(dishes)

            total_res += 1
            total_dish += len(dishes)
        
        self.stdout.write(
            self.style.SUCCESS(
                f"Uploaded {total_res} Restaurants & {total_dish} Dishes."
            )
        )
