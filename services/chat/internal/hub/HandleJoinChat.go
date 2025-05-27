package hub

import (
	"context"
	"encoding/json"

	"github.com/antoniotorresxd/chat/internal/models"
	"github.com/gorilla/websocket"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func handleJoinChat(conn *websocket.Conn, msgBytes []byte, hub *Hub) {
	type Payload struct {
		Event  string `json:"event"`
		RoomID string `json:"room_id"`
	}
	var data Payload
	if err := json.Unmarshal(msgBytes, &data); err != nil {
		sendError(conn, "Payload inválido para join_chat")
		return
	}

	roomObjID, err := primitive.ObjectIDFromHex(data.RoomID)
	if err != nil {
		sendError(conn, "RoomID inválido")
		return
	}

	// Verifica existencia del room
	var room models.ChatRoom
	if err := hub.roomsColl.FindOne(context.Background(), bson.M{"_id": roomObjID}).Decode(&room); err != nil {
		sendError(conn, "Sala no encontrada")
		return
	}

	// Opciones: los 10 mensajes más recientes, ordenados por created_at descendente
	findOptions := options.Find()
	findOptions.SetSort(bson.D{{"created_at", -1}})
	findOptions.SetLimit(10)

	cursor, err := hub.msgsColl.Find(
		context.Background(),
		bson.M{"room_id": roomObjID},
		findOptions,
	)
	if err != nil {
		sendError(conn, "Error al buscar mensajes")
		return
	}
	defer cursor.Close(context.Background())

	var messages []models.Message
	for cursor.Next(context.Background()) {
		var msg models.Message
		if err := cursor.Decode(&msg); err == nil {
			messages = append(messages, msg)
		}
	}
	// Invierte el slice para que queden del más antiguo al más reciente
	for i, j := 0, len(messages)-1; i < j; i, j = i+1, j-1 {
		messages[i], messages[j] = messages[j], messages[i]
	}

	resp := map[string]interface{}{
		"event":    "chat_history",
		"room_id":  data.RoomID,
		"messages": messages,
	}
	_ = conn.WriteJSON(resp)
}
