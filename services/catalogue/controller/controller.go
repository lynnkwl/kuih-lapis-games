package controller

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strconv"
	"github.com/gorilla/mux"
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
		log.Printf("Error finding games: %v", err)
	}

	var games []primitive.M

	for cur.Next(context.Background()){
		var game bson.M
		err := cur.Decode(&game)
		if err != nil {
			log.Printf("Error decoding game: %v", err)
			continue 
		}
		games = append(games, game)
	}

	defer cur.Close(context.Background())
	return games
}

//update one game
func updatePrice(gameId string, newPrice float64){
	id, _ := primitive.ObjectIDFromHex(gameId)
	filter := bson.M{"_id" : id}
	update := bson.M{"$set": bson.M{"Price": newPrice}}
	
	result, err := collection.UpdateOne(context.Background(), filter, update)
	if err != nil {
		log.Printf("error updating game price: %v", err)
		return
	}
	fmt.Println("Modified game!" , result.ModifiedCount)
}

//update availability
func updateAvailability(gameId string){
	id, _ := primitive.ObjectIDFromHex(gameId)
	filter := bson.M{"_id" : id}
	update := bson.M{"$set": bson.M{"Availability": "Available now"}}

	result, err := collection.UpdateOne(context.Background(), filter, update)
	if err != nil {
		log.Printf("error updating game availability: %v", err)
	}
	fmt.Println("Modified game!" , result.ModifiedCount)
}

//get one game by Id
func getOneGame (gameId string) bson.M{
	id, _ := primitive.ObjectIDFromHex(gameId)
	filter := bson.M{"_id" : id}
	
	result := collection.FindOne(context.Background(),filter)
	if result.Err() != nil {
		log.Printf("error finding game: %v", result.Err())
	}
	
	var game bson.M
	if err := result.Decode(&game); err != nil {
		log.Printf("error finding game: %v", err)
	}
	
	return game
}

//Actual controller - file

//get games
func GetMyAllGames (w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/x-www-form-urlencode")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	allGames := getAllGames()
	json.NewEncoder(w).Encode(allGames)
}

//update price
func UpdateMyPrice (w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    w.Header().Set("Access-Control-Allow-Methods", "PUT")

    // Get parameters from URL path using mux.Vars(r)
    params := mux.Vars(r)
    gameID := params["id"]
    newPriceStr := params["newp"]

    // Convert newPriceStr to an integer
    newPrice, err := strconv.ParseFloat(newPriceStr,64)
    if err != nil {
        http.Error(w, "Invalid price", http.StatusBadRequest)
        return
    }

    // Call updatePrice with the converted newPrice
    updatePrice(gameID, newPrice)

    response := map[string]string{"message": "Price updated successfully"}
    json.NewEncoder(w).Encode(response)
}

//update to available
func UpdateMyAvailability (w http.ResponseWriter, r *http.Request){
	w.Header().Set("Content-Type", "application/json")
    w.Header().Set("Access-Control-Allow-Methods", "PUT")
	params := mux.Vars(r)
	gameID := params["id"]

	// change availability
	updateAvailability(gameID)
	response := map[string]string{"message": "Price updated successfully"}
    json.NewEncoder(w).Encode(response)
}

//get one game by Id
func GetGameById (w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/x-www-form-urlencode")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	params := mux.Vars(r)
    gameID := params["id"]
	game := getOneGame(gameID)
	json.NewEncoder(w).Encode(game)
	fmt.Println("Got!")
}