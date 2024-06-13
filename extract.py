import csv
from faker import Faker
import random
import string
from google.cloud import storage

# Specify number of players to generate
num_players = 1000

# Create Faker instance
fake = Faker()

#List of games
games = ['Soccer', 'Basketball', 'Tennis', 'Baseball', 'Cricket', 'Hockey', 'Golf', 'Rugby', 'Volleyball']

# Define the character set for the password
password_characters = string.ascii_letters + string.digits + 'm'

# Generate player data and save it to a CSV file
with open('player_data.csv', mode='w', newline='') as file:
    fieldnames = ['player_id', 'first_name', 'last_name', 'email', 'game', 'phone_number', 'city', 'state', 'zipcode']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for i in range(1, num_players + 1):
        writer.writerow({
            "player_id": i,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "game" : random.choice(games),
            "phone_number": fake.phone_number(),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "zipcode": fake.zipcode()
        })

# Upload the CSV file to a GCS bucket
def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f'File {source_file_name} uploaded to {destination_blob_name} in {bucket_name}.')

# Set your GCS bucket name and destination file name
bucket_name = 'bkt-players-data'
source_file_name = 'players_data.csv'
destination_blob_name = 'players_data.csv'

# Upload the CSV file to GCS
upload_to_gcs(bucket_name, source_file_name, destination_blob_name)
