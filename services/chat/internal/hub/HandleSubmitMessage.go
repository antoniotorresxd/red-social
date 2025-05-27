package hub

import (
	"context"
	"encoding/json"
	"time"

	"github.com/antoniotorresxd/chat/internal/models"
	"github.com/gorilla/websocket"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

func handleSubmitMessage(conn *websocket.Conn, msgBytes []byte, hub *Hub) {
	type Payload struct {
		Event   string `json:"event"`
		RoomID  string `json:"room_id"`
		Sender  string `json:"sender"` // ObjectID string
		Message string `json:"message"`
	}
	var data Payload
	if err := json.Unmarshal(msgBytes, &data); err != nil {
		sendError(conn, "Payload inválido para submit_message")
		return
	}
	roomObjID, err := primitive.ObjectIDFromHex(data.RoomID)
	if err != nil {
		sendError(conn, "RoomID inválido")
		return
	}
	senderObjID, err := primitive.ObjectIDFromHex(data.Sender)
	if err != nil {
		sendError(conn, "SenderID inválido")
		return
	}
	if len(data.Message) == 0 {
		sendError(conn, "El mensaje no puede estar vacío")
		return
	}

	msg := models.Message{
		ID:        primitive.NewObjectID(),
		RoomID:    roomObjID,
		SenderID:  senderObjID,
		Text:      data.Message,
		CreatedAt: time.Now(),
	}
	_, err = hub.msgsColl.InsertOne(context.Background(), msg)
	if err != nil {
		sendError(conn, "No se pudo guardar el mensaje")
		return
	}

	resp := map[string]interface{}{
		"event":     "new_message",
		"room_id":   data.RoomID,
		"sender":    data.Sender,
		"message":   data.Message,
		"timestamp": msg.CreatedAt,
	}
	_ = conn.WriteJSON(resp)
}
