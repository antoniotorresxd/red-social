package hub

import (
	"encoding/json"
	"log"
	"time"

	"github.com/gorilla/websocket"
)

// Client representa una conexión activa de WebSocket
type Client struct {
	Conn *websocket.Conn
	Send chan []byte
	Hub  *Hub
}

// ReadPump lee mensajes desde la conexión WebSocket y los despacha al router de eventos.
func (c *Client) ReadPump() {
	defer func() {
		c.Hub.Unregister <- c
		c.Conn.Close()
	}()
	c.Conn.SetReadLimit(512)
	c.Conn.SetReadDeadline(time.Now().Add(60 * time.Second))
	c.Conn.SetPongHandler(func(string) error {
		c.Conn.SetReadDeadline(time.Now().Add(60 * time.Second))
		return nil
	})
	for {
		_, msg, err := c.Conn.ReadMessage()
		if err != nil {
			log.Println("WebSocket read error:", err)
			break
		}
		DispatchEvent(c, msg, c.Hub)
	}
}

// WritePump envía mensajes al cliente WebSocket
func (c *Client) WritePump() {
	ticker := time.NewTicker(54 * time.Second)
	defer func() {
		ticker.Stop()
		c.Conn.Close()
	}()
	for {
		select {
		case msg, ok := <-c.Send:
			c.Conn.SetWriteDeadline(time.Now().Add(10 * time.Second))
			if !ok {
				_ = c.Conn.WriteMessage(websocket.CloseMessage, []byte{})
				return
			}
			if err := c.Conn.WriteMessage(websocket.TextMessage, msg); err != nil {
				return
			}
		case <-ticker.C:
			c.Conn.SetWriteDeadline(time.Now().Add(10 * time.Second))
			if err := c.Conn.WriteMessage(websocket.PingMessage, nil); err != nil {
				return
			}
		}
	}
}

// DispatchEvent analiza el evento recibido y llama al handler correspondiente
func DispatchEvent(c *Client, msg []byte, hub *Hub) {
	var generic struct {
		Event string `json:"event"`
	}
	if err := json.Unmarshal(msg, &generic); err != nil {
		sendError(c.Conn, "Formato JSON inválido")
		return
	}
	switch generic.Event {
	case "create_chat":
		HandleCreateChat(c.Conn, msg, hub)
	case "join_chat":
		HandleJoinChat(c.Conn, msg, hub)
	case "submit_message":
		HandleSubmitMessage(c.Conn, msg, hub)
	case "list_chats":
		HandleListChats(c.Conn, msg, hub)
	default:
		sendError(c.Conn, "Evento desconocido: "+generic.Event)
	}
}

func sendError(conn *websocket.Conn, msg string) {
	resp := map[string]interface{}{
		"event":   "error",
		"message": msg,
	}
	_ = conn.WriteJSON(resp)
}
