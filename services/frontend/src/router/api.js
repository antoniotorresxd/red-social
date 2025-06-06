// Router api
import axios from 'axios';

const baseURL = "https://apigateway-mg13.onrender.com"
const wssURL = "ws://services-chat-4he7.onrender.com/ws/chat/" 

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
      "ws_chat": wssURL
    }

}


export default apiUrl
