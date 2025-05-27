package hub

import (
	"github.com/gorilla/websocket"
)

// ----------- HANDLER: CREAR CHAT -----------------
func HandleCreateChat(conn *websocket.Conn, msgBytes []byte, hub *Hub) {
	handleCreateChat(conn, msgBytes, hub)
}

// ----------- HANDLER: UNIRSE A CHAT Y LISTAR MENSAJES -------------
func HandleJoinChat(conn *websocket.Conn, msgBytes []byte, hub *Hub) {
	handleJoinChat(conn, msgBytes, hub)
}

// ----------- HANDLER: ENVIAR MENSAJE -------------------
func HandleSubmitMessage(conn *websocket.Conn, msgBytes []byte, hub *Hub) {
	handleSubmitMessage(conn, msgBytes, hub)
}

// ----------- HANDLER: LISTAR CHATS RECIENTES -------------------
func HandleListChats(conn *websocket.Conn, msgBytes []byte, hub *Hub) {
	handleListChats(conn, msgBytes, hub)
}
