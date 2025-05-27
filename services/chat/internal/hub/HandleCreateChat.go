package hub

import (
	"context"
	"encoding/json"
	"time"

	"github.com/antoniotorresxd/chat/internal/models"
	"github.com/gorilla/websocket"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

// Handler que crea una sala nueva entre dos participantes (o retorna la existente)
func handleCreateChat(conn *websocket.Conn, msgBytes []byte, hub *Hub) {
	type Payload struct {
		Event        string   `json:"event"`
		Participants []string `json:"participants"`
	}
	var data Payload
	if err := json.Unmarshal(msgBytes, &data); err != nil {
		sendError(conn, "Payload inválido para create_chat")
		return
	}

	if len(data.Participants) != 2 {
		sendError(conn, "Se requieren exactamente dos participantes")
		return
	}

	// Convertir participantes a ObjectID
	var participants []primitive.ObjectID
	for _, idStr := range data.Participants {
		objID, err := primitive.ObjectIDFromHex(idStr)
		if err != nil {
			sendError(conn, "ID de participante inválido")
			return
		}
		participants = append(participants, objID)
	}

	// Buscar chat existente (exactamente esos dos, en cualquier orden)
	filter := bson.M{"participants": bson.M{"$all": participants, "$size": 2}}
	var room models.ChatRoom
	err := hub.roomsColl.FindOne(context.Background(), filter).Decode(&room)
	if err == nil {
		resp := map[string]interface{}{
			"event":        "chat_exists",
			"room_id":      room.ID.Hex(),
			"participants": data.Participants,
		}
		_ = conn.WriteJSON(resp)
		return
	}

	// Crear nueva sala
	room.ID = primitive.NewObjectID()
	room.ParticipantIDs = participants
	_, err = hub.roomsColl.InsertOne(context.Background(), bson.M{
		"_id":          room.ID,
		"participants": participants,
		"created_at":   time.Now(),
		"updated_at":   time.Now(),
	})
	if err != nil {
		sendError(conn, "No se pudo crear la sala")
		return
	}

	resp := map[string]interface{}{
		"event":        "chat_created",
		"room_id":      room.ID.Hex(),
		"participants": data.Participants,
	}
	_ = conn.WriteJSON(resp)
}
