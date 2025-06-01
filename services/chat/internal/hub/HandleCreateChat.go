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
    "go.mongodb.org/mongo-driver/mongo"
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

    idToEmail, err := utils.GetEmailsForUsers(data.Participants, data.Token)
    if err != nil {
        sendError(conn, "No se pudieron obtener los correos")
        return
    }

    var participants []models.ChatParticipant
    var objectIDs []primitive.ObjectID

    for _, id := range data.Participants {
        objID, err := utils.GenerateObjectIDFromNumericID(id)
        if err != nil {
            sendError(conn, fmt.Sprintf("ID inválido: %s", id))
            return
        }
        email := idToEmail[id]
        participants = append(participants, models.ChatParticipant{
            ObjectID:  objID,
            NumericID: id,
            Email:     email,
        })
        objectIDs = append(objectIDs, objID)
    }

    // Revisa si ya existe un chat entre estos dos usuarios
    filter := bson.M{
        "participant_ids": bson.M{"$all": objectIDs},
        "participant_ids.2": bson.M{"$exists": false}, // para limitar a exactamente 2
    }

    var existing models.ChatRoom
    err = hub.roomsColl.FindOne(context.Background(), filter).Decode(&existing)
    if err == nil {
        // Chat ya existe
        resp := map[string]interface{}{
            "event":        "chat_exists",
            "room_id":      existing.ID.Hex(),
            "participants": []string{participants[0].Email, participants[1].Email},
        }
        _ = conn.WriteJSON(resp)
        return
    } else if err != mongo.ErrNoDocuments {
        sendError(conn, "Error al verificar chats existentes")
        return
    }

    roomID := primitive.NewObjectID()
    _, err = hub.roomsColl.InsertOne(context.Background(), bson.M{
        "_id":            roomID,
        "participants":   participants,
        "participant_ids": objectIDs,
        "created_at":     time.Now(),
        "updated_at":     time.Now(),
    })
    if err != nil {
        sendError(conn, "No se pudo crear el chat")
        return
    }

    resp := map[string]interface{}{
        "event":        "chat_created",
        "room_id":      roomID.Hex(),
        "participants": []string{participants[0].Email, participants[1].Email},
    }
    _ = conn.WriteJSON(resp)
}
