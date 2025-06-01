package hub

import (
	"github.com/gorilla/websocket"
)

// ----------- HANDLER: CREAR CHAT -----------------
func HandleCreateChat(conn *websocket.Conn, msgBytes []byte, hub *Hub) {
	// Sigue usando *websocket.Conn porque no necesita RoomID ni canal Send
	handleCreateChat(conn, msgBytes, hub)
}

// ----------- HANDLER: LISTAR CHATS RECIENTES -------------------
func HandleListChats(conn *websocket.Conn, msgBytes []byte, hub *Hub) {
	// Igual, no depende del contexto de un cliente específico
	handleListChats(conn, msgBytes, hub)
}

// ----------- HANDLER: UNIRSE A CHAT Y LISTAR MENSAJES -------------
func HandleJoinChat(client *Client, msgBytes []byte, hub *Hub) {
	// Ahora usa *Client porque maneja RoomID y canal Send
	handleJoinChat(client, msgBytes, hub)
}

// ----------- HANDLER: ENVIAR MENSAJE -------------------
func HandleSubmitMessage(client *Client, msgBytes []byte, hub *Hub) {
	// También usa *Client para hacer broadcast
	handleSubmitMessage(client, msgBytes, hub)
}
