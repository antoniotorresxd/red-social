// Router api
import axios from 'axios';

const baseURL = process.env.VUE_APP_URL
axios.defaults.baseURL = baseURL;

const apiUrl = {
    users: {
      "login"    : baseURL + "/microservice-users/login/",
      "register" : baseURL + "/microservice-users/register/",
      "logout"   : baseURL + "/microservice-users/logout/",
      "refresh"  : baseURL + "/microservice-users/token/refresh/",
      "user"     : baseURL + "/microservice-users/",
      "reset_password" : baseURL + "/microservice-users/reset-password/",
    },
    
    community: {
      "list"  : baseURL + "/microservice-community/",
      "create": baseURL + "/microservice-community/create/",
      "join"  : baseURL + "/microservice-community/join/",
      "exit"  : baseURL + "/microservice-community/exit/",
    },

    publication: {
      "publish": baseURL + "/microservice-publication/",
    },

}


export default apiUrl
