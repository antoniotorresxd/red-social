package utils

import (
	"crypto/md5"
	"encoding/hex"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

func GenerateObjectIDFromNumericID(numericID string) (primitive.ObjectID, error) {
	hasher := md5.New()
	hasher.Write([]byte(numericID))
	hash := hex.EncodeToString(hasher.Sum(nil))
	return primitive.ObjectIDFromHex(hash[:24])
}
