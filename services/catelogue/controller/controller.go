package controller

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

const connectionString = "mongodb+srv://lynnkwl:test123@gaames.bta3w6g.mongodb.net/?retryWrites=true&w=majority&appName=Gaames"
const dbName = "games"
const colName = "games"

var collection *mongo.Collection

//connect with MongoDB

func init(){
	//client option
	clientOption := options.Client().ApplyURI(connectionString)
	//connect to mongoDB
	client, err := mongo.Connect(context.TODO(), clientOption)

	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("Mongo connection success!")

	collection = client.Database(dbName).Collection(colName)

	//collection instance 
	fmt.Println("Collection instance is ready")
}

//get all games from mongo
func getAllGames() []primitive.M {
	cur, err := collection.Find(context.Background(), bson.D{})
	if err != nil {
		log.Fatal(err)
	}

	var games []primitive.M

	for cur.Next(context.Background()){
		var game bson.M
		err := cur.Decode(&game)
		if err != nil {
			log.Fatal(err)
		}
		games = append(games, game)
	}

	defer cur.Close(context.Background())
	return games
}

//Actual controller - file

func GetMyAllGames (w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/x-www-form-urlencode")
	allGames := getAllGames()
	json.NewEncoder(w).Encode(allGames)
}