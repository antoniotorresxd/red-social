package main

import (
	"log"
	"net/http"
	"os"

	"github.com/antoniotorresxd/chat/internal/db"
	"github.com/antoniotorresxd/chat/internal/hub"
	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true // Ajusta tu política de CORS aquí
	},
}

func serveWs(h *hub.Hub, w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("serveWs: upgrade error:", err)
		return
	}
	client := &hub.Client{
		Conn: conn,
		Send: make(chan []byte, 256),
		Hub:  h,
	}
	h.Register <- client

	go client.WritePump()
	go client.ReadPump()
}

func main() {
	database := db.Connect()
	roomsColl := database.Collection("rooms")
	msgsColl := database.Collection("messages")

	h := hub.NewHub(roomsColl, msgsColl)
	go h.Run()

	http.HandleFunc("/ws/chat/", func(w http.ResponseWriter, r *http.Request) {
		serveWs(h, w, r)
	})

	port := os.Getenv("PORT")
	if port == "" {
		port = "8004"
	}

	log.Printf("Chat service listening on:%s/ws/chat/", port)
	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatal("ListenAndServe:", err)
	}

}
