package hub

import (
	"sync"

	"go.mongodb.org/mongo-driver/mongo"
)

// gestionar clientes y el broadcast de mensajes
type Hub struct {
	Clients    map[*Client]bool
	Broadcast  chan []byte
	Register   chan *Client
	Unregister chan *Client

	roomsColl *mongo.Collection
	msgsColl  *mongo.Collection

	mu sync.Mutex
}

// NewHub 
func NewHub(roomsColl, msgsColl *mongo.Collection) *Hub {
	return &Hub{
		Clients:    make(map[*Client]bool),
		Broadcast:  make(chan []byte),
		Register:   make(chan *Client),
		Unregister: make(chan *Client),
		roomsColl:  roomsColl,
		msgsColl:   msgsColl,
	}
}

// Run ejecuta el ciclo principal del Hub
func (h *Hub) Run() {
	for {
		select {
		case client := <-h.Register:
			h.mu.Lock()
			h.Clients[client] = true
			h.mu.Unlock()

		case client := <-h.Unregister:
			h.mu.Lock()
			if _, ok := h.Clients[client]; ok {
				delete(h.Clients, client)
				close(client.Send)
			}
			h.mu.Unlock()

		case msg := <-h.Broadcast:
			h.mu.Lock()
			for c := range h.Clients {
				select {
				case c.Send <- msg:
				default:
					close(c.Send)
					delete(h.Clients, c)
				}
			}
			h.mu.Unlock()
		}
	}
}
