package models

import (
    "time"

    "go.mongodb.org/mongo-driver/bson/primitive"
)

// ChatRoom representa una sala y sus participantes
type ChatRoom struct {
    ID             primitive.ObjectID   `bson:"_id,omitempty"`
    ParticipantIDs []primitive.ObjectID `bson:"participants"`
}

// Message representa un mensaje en una sala
type Message struct {
    ID        primitive.ObjectID `bson:"_id,omitempty"`
    RoomID    primitive.ObjectID `bson:"room_id"`
    SenderID  primitive.ObjectID `bson:"sender_id"`
    Text      string             `bson:"text"`
    CreatedAt time.Time          `bson:"created_at"`
}
