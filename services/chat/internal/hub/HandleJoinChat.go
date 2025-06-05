package hub

import (
	"context"
	"encoding/json"
	"log"
	"time"

	"github.com/antoniotorresxd/chat/internal/models"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func handleJoinChat(client *Client, msgBytes []byte, hub *Hub) {
	type Payload struct {
		Event  string `json:"event"`
		RoomID string `json:"room_id"`
	}

	var data Payload
	if err := json.Unmarshal(msgBytes, &data); err != nil {
		sendError(client.Conn, "Payload inválido para join_chat")
		return
	}

	roomObjID, err := primitive.ObjectIDFromHex(data.RoomID)
	if err != nil {
		sendError(client.Conn, "RoomID inválido")
		return
	}

	var room models.ChatRoom
	if err := hub.roomsColl.FindOne(context.Background(), bson.M{"_id": roomObjID}).Decode(&room); err != nil {
		sendError(client.Conn, "Sala no encontrada")
		return
	}

	client.RoomID = data.RoomID

	findOptions := options.Find().SetSort(bson.D{{Key: "created_at", Value: -1}}).SetLimit(100)
	cursor, err := hub.msgsColl.Find(context.Background(), bson.M{"room_id": roomObjID}, findOptions)
	if err != nil {
		sendError(client.Conn, "Error al buscar mensajes")
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

	for i, j := 0, len(messages)-1; i < j; i, j = i+1, j-1 {
		messages[i], messages[j] = messages[j], messages[i]
	}

	var formattedMessages []map[string]interface{}
	for _, m := range messages {
		senderNumericID := ""
		for _, p := range room.Participants {
			if p.ObjectID == m.SenderID {
				senderNumericID = p.NumericID
				break
			}
		}

		formattedMessages = append(formattedMessages, map[string]interface{}{
			"_id":        m.ID.Hex(),
			"sender_id":  senderNumericID, 
			"message":    m.Text,
			"timestamp":  m.CreatedAt.Format(time.RFC3339),
		})
	}

	resp := map[string]interface{}{
		"event":    "chat_history",
		"room_id":  data.RoomID,
		"messages": formattedMessages,
	}
	if err := client.Conn.WriteJSON(resp); err != nil {
		log.Println("Error al enviar historial de chat:", err)
	}
}
