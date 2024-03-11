import json
import pymongo

myclient= pymongo.MongoClient("mongodb+srv://lynnkwl:test123@gaames.bta3w6g.mongodb.net/?retryWrites=true&w=majority&appName=Gaames")
mydb = myclient["games"]
mycol = mydb["games"]



# Assuming the JSON data is stored in a variable called 'json_data'
# If the JSON data is in a file, you can read it like this:
with open('./released_games.json', 'r') as file:
    json_data = json.load(file)


# Initialize an empty list to store the extracted information
extracted_info = []

for result in json_data['results']:
    for hit in result['hits']:
        extracted_info.append ({
            'GameName' : hit['title'],
            'Price' : hit['price'],
            'CoverArt' :  'https://assets.nintendo.com/image/upload/ar_16:9,b_auto:border,c_lpad/b_white/f_auto/q_auto/dpr_2.0/c_scale,w_300/' + hit['productImage'],
            'Url' : hit['url'],
            'Genre' : hit['genres'],
            'ReleaseDate' : hit['releaseDate'],
            'Description' : hit['description'],
            'Availability' : hit['availability'],
            'Publisher' : hit['softwarePublisher'],
            'Developer' : hit['softwareDeveloper'],
            'Platform' : hit['corePlatforms'],
            'Quantity' : 100
            })

x = mycol.insert_many(extracted_info[0:50])

print(x.inserted_ids)