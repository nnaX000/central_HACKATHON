import csv
from django.core.management.base import BaseCommand
from character.models import (
    Food,
    CleaningSpot,
    WalkingPlace,
)  # character 앱의 models 모듈에서 모델을 가져옵니다.


class Command(BaseCommand):
    help = "Load data from CSV files"

    def handle(self, *args, **kwargs):
        self.load_foods()
        self.load_cleaning_spots()
        self.load_walking_places()

    def load_foods(self):
        with open("character/foods.csv", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if row:  # 빈 줄 무시
                    Food.objects.create(name=row[0])

    def load_cleaning_spots(self):
        with open("character/cleaning_spot.csv", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if row:  # 빈 줄 무시
                    CleaningSpot.objects.create(name=row[0])

    def load_walking_places(self):
        with open("character/sports.csv", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if row:  # 빈 줄 무시
                    WalkingPlace.objects.create(name=row[0])
