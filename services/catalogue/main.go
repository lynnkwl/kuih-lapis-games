package main

import (
	"fmt"
	"net/http"
	"github.com/lynnkwl/kuih-lapis-games/router"
)

func main() {
	r := router.Router()
	fmt.Println("Server is getting started...")
	http.ListenAndServe(":4300", r)
	fmt.Println("Listening!")
}