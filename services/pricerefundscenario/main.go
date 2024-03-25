package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"strconv"
)

func main() {
	fmt.Println("yess hello")
	
	//change price in catalogue
	// err := performChangePrice("65f70af855a3471d6f767862", 30.00)
	// if err != nil {
	// 	fmt.Printf("Error updating game price: %v\n", err)
	// }

	// //calculate the difference
	// response , err := getPriceDiff("65f70af855a3471d6f767862", 20.00)
	// if err != nil {
	// 	fmt.Printf("Error calculating difference: %v\n", err)
	// }
	// var priceDiff = response

	// email
	err := sendEmail ("65f70af855a3471d6f767862", 20.00)
	if err != nil {
		fmt.Printf("Error sending email %v\n", err)
		}
}

//getting price difference

func getPriceDiff(gameID string, newPrice float64) (float64, error) {
	url := "http://localhost:4300/api/getgame/" + gameID
    request, err := http.NewRequest(http.MethodGet, url, nil)
    if err != nil {
        return 0, fmt.Errorf("error creating request: %v", err)
    }

    // Send the request using http.Client.
    client := &http.Client{}
    response, err := client.Do(request)
    if err != nil {
        return 0, fmt.Errorf("error sending request: %v", err)
    }
    defer response.Body.Close()

    // Check the HTTP response status code.
    if response.StatusCode != http.StatusOK {
        return 0, fmt.Errorf("received non-ok HTTP status: %s", response.Status)
    }

    // Read the response body
    body, err := ioutil.ReadAll(response.Body)
    if err != nil {
        return 0, fmt.Errorf("error reading response body: %v", err)
    }

    // Define a struct to unmarshal the JSON response
    var gameData struct {
        Price float64 `json:"Price"`
    }

    // Unmarshal the JSON response into the struct
    if err := json.Unmarshal(body, &gameData); err != nil {
        return 0, fmt.Errorf("error unmarshaling JSON response: %v", err)
    }

    // Return the price extracted from the JSON response
    return (gameData.Price - newPrice) , nil
}

//changing price in DB

func performChangePrice(gameId string, newPrice float64) error{
	// newPriceStr := fmt.Sprintf("%.2f", newPrice)
	newPriceStr  := strconv.FormatFloat(newPrice, 'f', -1, 64)
	url := "http://localhost:4300/api/games/updatePrice/" + gameId + "/" + newPriceStr
	fmt.Println(url)
	
	request, err := http.NewRequest(http.MethodPut, url, nil)
	if err != nil {
		return fmt.Errorf("error creating request: %v", err)
	}

	// Send the request using http.Client.
	client := &http.Client{}
	response, err := client.Do(request)
	if err != nil {
		return fmt.Errorf("error sending request: %v", err)
	}
	defer response.Body.Close()

	// Check the HTTP response status code.
	if response.StatusCode != http.StatusOK {
		return fmt.Errorf("received non-ok HTTP status: %s", response.Status)
	}

	// If you need to read the response body, you can do so here.
	// If the response body is not needed, you can ignore this part.

	fmt.Printf("Successfully updated price for game ID %s to %s\n", gameId, newPriceStr)
	return nil
}

//sending notification email
func sendEmail(gameId string, newPrice float64) error {
	type Email struct {
		CustomerAddress string `json:"customer_address"`
		EmailSubject    string `json:"email_subject"`
		EmailBody       string `json:"email_body"`
	}

	// response, err := getPriceDiff("65f70af855a3471d6f767862", 20.00)
	// if err != nil {
	// 	fmt.Printf("Error calculating difference: %v\n", err)
	// }
	// var priceDiff = response
	var customerEmail = "lynn.khoo.2022@scis.smu.edu.sg"
	var emailSubject string = "Refund processed for game: "
	var emailBody string = "Hello Lynn, your refund of has processed!"

	m := Email{
		CustomerAddress: customerEmail,
		EmailSubject:    emailSubject,
		EmailBody:       emailBody,
	}

	b, err := json.Marshal(m)
	if err != nil {
		return fmt.Errorf("error marshaling JSON: %v", err)
	}

	url := "http://localhost:5000/send_email"

	request, err := http.NewRequest(http.MethodPost, url, bytes.NewBuffer(b))
	if err != nil {
		return fmt.Errorf("error creating request: %v", err)
	}

	// Set the content type header to application/json
	request.Header.Set("Content-Type", "application/json")

	// Send the request using http.Client.
	client := &http.Client{}
	response2, err := client.Do(request)
	if err != nil {
		return fmt.Errorf("error sending request: %v", err)
	}
	defer response2.Body.Close()

	// Check the HTTP response status code.
	if response2.StatusCode != http.StatusOK {
		return fmt.Errorf("received non-ok HTTP status: %s", response2.Status)
	}

	// If you need to read the response body, you can do so here.
	// If the response body is not needed, you can ignore this part.

	fmt.Println("Successfully sent email", gameId)
	return nil
}



