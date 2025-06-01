package utils

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
    "strings"
    "log"
)

type UserEmail struct {
    ID    interface{} `json:"id"`
    Email string      `json:"email"`
}

func GetEmailsForUsers(ids []string, token string) (map[string]string, error) {
    idsParam := strings.Join(ids, ",")
    url := fmt.Sprintf("http://gateway/microservice-users/?ids=%s", idsParam)
    log.Println("URL llamada:", url)
    log.Println("Token enviado:", token)

    req, err := http.NewRequest("GET", url, nil)
    if err != nil {
        return nil, err
    }

    req.Header.Set("Authorization", "Bearer "+token)

    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        return nil, err
    }
    log.Println("Respuesta HTTP:", string(body))

    if resp.StatusCode != 200 {
        return nil, fmt.Errorf("HTTP error: %d, respuesta: %s", resp.StatusCode, string(body))
    }

    var data struct {
        Data []UserEmail `json:"data"`
    }
    if err := json.Unmarshal(body, &data); err != nil {
        return nil, err
    }

    result := make(map[string]string)
    for _, u := range data.Data {
        result[fmt.Sprintf("%v", u.ID)] = u.Email
    }

    log.Println(result)
    return result, nil
}

