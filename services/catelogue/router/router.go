package router

import (
	"github.com/gorilla/mux"
	"github.com/lynnkwl/kuih-lapis-games/controller"
)

func Router() *mux.Router {
	router := mux.NewRouter()

	router.HandleFunc("/api/games", controller.GetMyAllGames).Methods("GET")

	return router
}