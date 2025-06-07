// Router api
import axios from 'axios';

// const host = import.meta.env.VITE_API_URL
// const protocol = import.meta.env.VITE_API_PROTOCOL
// const wssProtocol = import.meta.env.VITE_WSS_PROTOCOL

const host = "service-gateway-cedfc8huebcbdwad.mexicocentral-01.azurewebsites.net"
const protocol = "https"
const wssProtocol = "wss"


const baseURL = `${protocol}://${host}`
const wssURL = `${wssProtocol}://${host}`

axios.defaults.baseURL = baseURL;

const apiUrl = {
    users: {
      "login"    : baseURL + "/microservice-users/login/",
      "register" : baseURL + "/microservice-users/register/",
      "logout"   : baseURL + "/microservice-users/logout/",
      "refresh"  : baseURL + "/microservice-users/token/refresh/",
      "user"     : baseURL + "/microservice-users/",
      "reset_password" : baseURL + "/microservice-users/reset-password/",
      "find_by_email"  : baseURL + "/microservice-users/find-by-email/",
    },
    
    community: {
      "list"  : baseURL + "/microservice-community/",
      "create": baseURL + "/microservice-community/create/",
      "join"  : baseURL + "/microservice-community/join/",
      "exit"  : baseURL + "/microservice-community/exit/",
    },

    publication: {
      "publish"    : baseURL + "/microservice-publication/",
      "submit_task": baseURL + "/microservice-publication/submit-task/",
      "add_comment": baseURL + "/microservice-publication/add-comment/",
    },

    chat: {
      "ws_chat": wssURL + "/ws/chat/",
    }

}


export default apiUrl
