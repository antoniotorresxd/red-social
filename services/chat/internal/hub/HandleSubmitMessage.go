package hub

import (
	"context"
	"encoding/json"
	"log"
	"time"

	"github.com/antoniotorresxd/chat/internal/models"
	"github.com/antoniotorresxd/chat/internal/utils"

	"go.mongodb.org/mongo-driver/bson/primitive"
)

func handleSubmitMessage(client *Client, msgBytes []byte, hub *Hub) {
	type Payload struct {
		Event   string `json:"event"`
		RoomID  string `json:"room_id"`
		Sender  string `json:"sender"`  // Hex string
		Message string `json:"message"`
	}

	var data Payload
	if err := json.Unmarshal(msgBytes, &data); err != nil {
		sendError(client.Conn, "Payload inválido para submit_message")
		return
	}

	// Validaciones básicas
	if len(data.Message) == 0 {
		sendError(client.Conn, "El mensaje no puede estar vacío")
		return
	}

	roomObjID, err := primitive.ObjectIDFromHex(data.RoomID)
	if err != nil {
		sendError(client.Conn, "RoomID inválido")
		return
	}

	senderObjID, err := utils.GenerateObjectIDFromNumericID(data.Sender)
	if err != nil {
		sendError(client.Conn, "Sender inválido")
		return
	}
	
	// Verifica que el cliente esté en la sala
	if client.RoomID != data.RoomID {
		sendError(client.Conn, "No estás unido a esta sala")
		return
	}

	// Guardar el mensaje
	msg := models.Message{
		ID:        primitive.NewObjectID(),
		RoomID:    roomObjID,
		SenderID:  senderObjID,
		Text:      data.Message,
		CreatedAt: time.Now(),
	}
	if _, err := hub.msgsColl.InsertOne(context.Background(), msg); err != nil {
		sendError(client.Conn, "No se pudo guardar el mensaje")
		return
	}

	// Armar payload de respuesta
	resp := map[string]interface{}{
		"event":     "new_message",
		"room_id":   data.RoomID,
		"sender":    data.Sender,
		"message":   data.Message,
		"timestamp": msg.CreatedAt,
	}
	msgBytesOut, _ := json.Marshal(resp)

	hub.mu.Lock()
	defer hub.mu.Unlock()

	if len(hub.Clients) == 0 {
		log.Println("⚠️ No hay clientes registrados en el Hub")
		return
	}

	for c := range hub.Clients {
		if c.RoomID == data.RoomID {
			c.Send <- msgBytesOut
		}
	}
}
