package hub

import (
	"context"
	"encoding/json"

	"github.com/antoniotorresxd/chat/internal/models"
	"github.com/gorilla/websocket"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

func handleListChats(conn *websocket.Conn, msgBytes []byte, hub *Hub) {
	type Payload struct {
		Event string `json:"event"`
		User  string `json:"user"` // ObjectID string
	}
	var data Payload
	if err := json.Unmarshal(msgBytes, &data); err != nil {
		sendError(conn, "Payload inválido para list_chats")
		return
	}
	userObjID, err := primitive.ObjectIDFromHex(data.User)
	if err != nil {
		sendError(conn, "UserID inválido")
		return
	}

	cursor, err := hub.roomsColl.Find(context.Background(), bson.M{"participants": userObjID})
	if err != nil {
		sendError(conn, "Error al buscar salas")
		return
	}
	defer cursor.Close(context.Background())

	var rooms []models.ChatRoom
	for cursor.Next(context.Background()) {
		var r models.ChatRoom
		if err := cursor.Decode(&r); err == nil {
			rooms = append(rooms, r)
		}
	}
	// Opcional: limitar a 10, ordenar por updated_at
	if len(rooms) > 10 {
		rooms = rooms[len(rooms)-10:]
	}

	resp := map[string]interface{}{
		"event": "chats_list",
		"chats": rooms,
	}
	_ = conn.WriteJSON(resp)
}
