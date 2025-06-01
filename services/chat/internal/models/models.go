package models

import (
    "time"

    "go.mongodb.org/mongo-driver/bson/primitive"
)

type ChatParticipant struct {
    ObjectID   primitive.ObjectID `bson:"object_id"`
    NumericID  string             `bson:"numeric_id"`
    Email      string             `bson:"email"` 
}

type ChatRoom struct {
    ID           primitive.ObjectID   `bson:"_id,omitempty"`
    Participants []ChatParticipant    `bson:"participants"`
}

type Message struct {
    ID         primitive.ObjectID `bson:"_id,omitempty"`
    RoomID     primitive.ObjectID `bson:"room_id"`
    SenderID   primitive.ObjectID `bson:"sender_id"`
    SenderEmail string            `bson:"sender_email"`
    Text       string             `bson:"text"`
    CreatedAt  time.Time          `bson:"created_at"`
}

