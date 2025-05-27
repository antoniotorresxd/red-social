package db

import (
    "context"
    "log"
    "os"
    "time"

    "go.mongodb.org/mongo-driver/mongo"
    "go.mongodb.org/mongo-driver/mongo/options"
)

func Connect() *mongo.Database {
    uri := os.Getenv("MONGO_URI")
    if uri == "" {
        log.Fatal("MONGO_URI no está definido")
    }
    dbName := os.Getenv("MONGO_DB")
    if dbName == "" {
        log.Fatal("MONGO_DB no está definido")
    }

    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()

    clientOpts := options.Client().ApplyURI(uri)
    client, err := mongo.Connect(ctx, clientOpts)
    if err != nil {
        log.Fatalf("error conectando a Mongo: %v", err)
    }

    if err := client.Ping(ctx, nil); err != nil {
        log.Fatalf("no se pudo hacer ping a Mongo: %v", err)
    }

    log.Println("✅ Conectado a MongoDB:", uri)
    return client.Database(dbName)
}
