package hub

import (
    "context"
    "encoding/json"

    "github.com/antoniotorresxd/chat/internal/models"
    "github.com/antoniotorresxd/chat/internal/utils"
    "github.com/gorilla/websocket"
    "go.mongodb.org/mongo-driver/bson"
)

func handleListChats(conn *websocket.Conn, msgBytes []byte, hub *Hub) {
    type Payload struct {
        Event string `json:"event"`
        User  string `json:"user"` // ID numérico como string
    }

    var data Payload
    if err := json.Unmarshal(msgBytes, &data); err != nil {
        sendError(conn, "Payload inválido para list_chats")
        return
    }

    userObjID, err := utils.GenerateObjectIDFromNumericID(data.User)
    if err != nil {
        sendError(conn, "ID de usuario inválido")
        return
    }

    filter := bson.M{"participant_ids": userObjID}

    cursor, err := hub.roomsColl.Find(context.Background(), filter)
    if err != nil {
        sendError(conn, "No se pudieron obtener los chats")
        return
    }
    defer cursor.Close(context.Background())

    var chats []models.ChatRoom
    if err := cursor.All(context.Background(), &chats); err != nil {
        sendError(conn, "Error al leer datos de chats")
        return
    }

    var responseChats []map[string]interface{}
    for _, chat := range chats {
        var emails []string
        for _, p := range chat.Participants {
            emails = append(emails, p.Email)
        }

        responseChats = append(responseChats, map[string]interface{}{
            "_id":          chat.ID.Hex(),
            "participants": emails,
        })
    }

    resp := map[string]interface{}{
        "event": "chats_list",
        "chats": responseChats,
    }

    _ = conn.WriteJSON(resp)
}
