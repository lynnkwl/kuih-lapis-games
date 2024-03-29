import json
import pymongo
import stripe

stripe.api_key = "sk_test_51OrKLBJvTzYZwoklWyczOfr18VRIBOiZSBNuVwGfoSUMHpG1O0TSWW24Q4BClFu0v3B4v4fOuFYsatEtW1MZHNc500KElhXUDE"
myclient= pymongo.MongoClient("mongodb+srv://lynnkwl:test123@gaames.bta3w6g.mongodb.net/?retryWrites=true&w=majority&appName=Gaames")
mydb = myclient["games"]
mycol = mydb["games"]



# Assuming the JSON data is stored in a variable called 'json_data'
# If the JSON data is in a file, you can read it like this:
with open('database/upcominggames.json', 'r') as file:
    json_data = json.load(file)


# Initialize an empty list to store the extracted information
extracted_info = []

for result in json_data['results']:
    for hit in result['hits']:
        if "Coming soon" in hit['availability']:
            extracted_info.append ({
                'GameName' : hit['title'],
                'StripePrice' : 
                stripe.Price.create(
                currency="sgd",
                unit_amount=int(hit['price']['regPrice']*100),
                recurring=None,
                product_data={"name": hit['title']},
                ),
                'Price' :  hit['price']['regPrice'],
                'CoverArt' :  'https://assets.nintendo.com/image/upload/ar_16:9,b_auto:border,c_lpad/b_white/f_auto/q_auto/dpr_2.0/c_scale,w_300/' + hit['productImage'],
                'Url' : hit['url'],
                'Genre' : hit['genres'],
                'ReleaseDate' : hit['releaseDate'],
                'Description' : hit['description'],
                'Availability' : "Coming Soon",
                'Publisher' : hit['softwarePublisher'],
                'Developer' : hit['softwareDeveloper'],
                'Platform' : hit['corePlatforms'],
                'Quantity' : 100
                })

x = mycol.insert_many(extracted_info)

print(x.inserted_ids)