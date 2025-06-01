package hub

import (
    "context"
    "encoding/json"
    "fmt"
    "time"

    "github.com/antoniotorresxd/chat/internal/models"
    "github.com/antoniotorresxd/chat/internal/utils"
    "github.com/gorilla/websocket"
    "go.mongodb.org/mongo-driver/bson"
    "go.mongodb.org/mongo-driver/bson/primitive"
)

func handleCreateChat(conn *websocket.Conn, msgBytes []byte, hub *Hub) {
    type Payload struct {
        Event        string   `json:"event"`
        Participants []string `json:"participants"` 
        Token        string   `json:"token"`      
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

    // Obtener emails de participantes usando el token recibido
    idToEmail, err := utils.GetEmailsForUsers(data.Participants, data.Token)
    if err != nil {
        sendError(conn, "No se pudieron obtener los emails de los participantes")
        return
    }

    // Crear slice de ChatParticipant con ObjectID, NumericID y Email
    var participants []models.ChatParticipant
    for _, idStr := range data.Participants {
        objID, err := utils.GenerateObjectIDFromNumericID(idStr)
        if err != nil {
            sendError(conn, fmt.Sprintf("Error al generar ObjectID: %s", err))
            return
        }
        email := idToEmail[idStr]
        participants = append(participants, models.ChatParticipant{
            ObjectID:  objID,
            NumericID: idStr,
            Email:     email,
        })
    }

    // Buscar si ya existe un chat entre esos dos participantes
    objectIDs := []primitive.ObjectID{participants[0].ObjectID, participants[1].ObjectID}
    filter := bson.M{"participants.object_id": bson.M{"$all": objectIDs}, "participants": bson.M{"$size": 2}}
    var room models.ChatRoom
    err = hub.roomsColl.FindOne(context.Background(), filter).Decode(&room)
    if err == nil {
        resp := map[string]interface{}{
            "event":        "chat_exists",
            "room_id":      room.ID.Hex(),
            "participants": []string{participants[0].Email, participants[1].Email},
        }
        _ = conn.WriteJSON(resp)
        return
    }

    room.ID = primitive.NewObjectID()
    room.Participants = participants
    _, err = hub.roomsColl.InsertOne(context.Background(), bson.M{
        "_id":         room.ID,
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
        "participants": []string{participants[0].Email, participants[1].Email},
    }
    _ = conn.WriteJSON(resp)
}
