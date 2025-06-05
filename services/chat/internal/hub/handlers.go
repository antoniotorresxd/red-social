package hub

import (
	"github.com/gorilla/websocket"
)

// ----------- HANDLER: CREAR CHAT -----------------
func HandleCreateChat(conn *websocket.Conn, msgBytes []byte, hub *Hub) {
	handleCreateChat(conn, msgBytes, hub)
}

// ----------- HANDLER: LISTAR CHATS RECIENTES -------------------
func HandleListChats(conn *websocket.Conn, msgBytes []byte, hub *Hub) {
	handleListChats(conn, msgBytes, hub)
}

// ----------- HANDLER: UNIRSE A CHAT Y LISTAR MENSAJES -------------
func HandleJoinChat(client *Client, msgBytes []byte, hub *Hub) {
	handleJoinChat(client, msgBytes, hub)
}

// ----------- HANDLER: ENVIAR MENSAJE -------------------
func HandleSubmitMessage(client *Client, msgBytes []byte, hub *Hub) {
	handleSubmitMessage(client, msgBytes, hub)
}
