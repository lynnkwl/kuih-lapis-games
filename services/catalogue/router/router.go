package router

import (
	"github.com/gorilla/mux"
	"github.com/lynnkwl/kuih-lapis-games/controller"
)

func Router() *mux.Router {
	router := mux.NewRouter()

	router.HandleFunc("/api/games", controller.GetMyAllGames).Methods("GET")
	router.HandleFunc("/api/games/updatePrice/{id}/{newp}", controller.UpdateMyPrice).Methods("PUT")
	router.HandleFunc("/api/games/updateAvailability/{id}", controller.UpdateMyAvailability).Methods("PUT")
	router.HandleFunc("/api/getgame/{id}", controller.GetGameById).Methods("GET")
	return router
}