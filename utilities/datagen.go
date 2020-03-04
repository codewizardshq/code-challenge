package main

import (
	"bytes"
	"database/sql"
	"encoding/json"
	"flag"
	"github.com/Pallinder/go-randomdata"
	"github.com/go-sql-driver/mysql"
	_ "github.com/go-sql-driver/mysql"
	"io/ioutil"
	"log"
	"net/http"
	"net/http/cookiejar"
	"strconv"
	"strings"
)

var (
	apiServer *string
	dbUser    *string
	dbHost    *string
	dbPass    *string
	dbName    *string
)

var pythonAnswer = `
print('76128', end='')
`

var jsAnswer = `
let output = '76128'
`

type User struct {
	Username         string `json:"username"`
	StudentFirstName string `json:"studentFirstName"`
	StudentLastName  string `json:"studentLastName"`
	StudentEmail     string `json:"studentEmail"`
	ParentFirstName  string `json:"parentFirstName"`
	ParentLastName   string `json:"parentLastName"`
	DOB              string `json:"DOB"`
	ParentEmail      string `json:"parentEmail"`
	Password         string `json:"password"`
	rank             int
	client           *http.Client
}

type Answer struct {
	rank          int
	correctAnswer string
}

func endpoint(path string) string {
	if !strings.HasPrefix(path, "/") {
		path = "/" + path
	}
	return *apiServer + path
}

func jsonDecode(jsonBytes []byte) map[string]interface{} {
	var i map[string]interface{}
	err := json.Unmarshal(jsonBytes, &i)
	if err != nil {
		panic(err)
	}
	return i
}

func jsonEncode(v interface{}) []byte {

	data, err := json.Marshal(v)

	if err != nil {
		panic(err)
	}

	return data
}

func (user *User) register() interface{} {

	req := jsonEncode(*user)

	res, err := user.client.Post(endpoint("/api/v1/users/register"),
		"application/json", bytes.NewBuffer(req))
	if err != nil {
		panic(err)
	}

	body, err := ioutil.ReadAll(res.Body)
	defer res.Body.Close()

	if err != nil {
		panic(err)
	}

	if res.StatusCode != 200 {
		log.Fatalf("register() failed. response: %s\n", body)
	}

	data := jsonDecode(body)

	log.Printf("registered new user %s\n", user.Username)

	return data
}

func (user *User) login() interface{} {

	login := map[string]string{
		"username": user.Username,
		"password": user.Password,
	}

	req := jsonEncode(login)
	res, _ := user.client.Post(endpoint("/api/v1/users/token/auth"), "application/json", bytes.NewBuffer(req))

	body, err := ioutil.ReadAll(res.Body)
	defer res.Body.Close()

	if err != nil {
		panic(err)
	}

	if res.StatusCode != 200 {
		log.Fatalf("login() failed: \n%s\n", body)
	}

	data := jsonDecode(body)

	user.hello()

	log.Printf("%s is rank %d", user.Username, user.rank)
	return data
}

func (user *User) GetJSON(url string) (map[string]interface{}, int) {

	res, err := user.client.Get(endpoint(url))

	if err != nil {
		panic(err.Error())
	}

	body, err := ioutil.ReadAll(res.Body)

	if err != nil {
		panic(err.Error())
	}
	defer res.Body.Close()

	if res.StatusCode == 500 {
		log.Fatalf("Internal Server Error: %s\n", body)
	}

	data := jsonDecode(body)

	return data, res.StatusCode
}

func (user *User) PostJSON(url string, data map[string]interface{}) (map[string]interface{}, int) {

	res, err := user.client.Post(endpoint(url), "application/json", bytes.NewBuffer(jsonEncode(data)))

	if err != nil {
		panic(err.Error())
	}

	body, err := ioutil.ReadAll(res.Body)

	defer res.Body.Close()

	if err != nil {
		panic(err.Error())
	}

	if res.StatusCode == 500 {
		log.Fatalf("Internal Server Error: %s\n", body)
	}

	return jsonDecode(body), res.StatusCode
}

func (user *User) hello() {

	data, status := user.GetJSON("/api/v1/users/hello")
	if status != 200 {
		log.Fatalf("hello() failed: %s", data)
	}
	user.rank = int(data["rank"].(float64))
}

func (user *User) answer(answer string) {

	log.Printf("%s answering question for rank %d", user.Username, user.rank)
	req := map[string]interface{}{
		"text": answer,
	}

	data, status := user.PostJSON("/api/v1/questions/answer", req)

	if status != 200 {
		log.Fatalf("answer() failed: %s\n", data)
	}

	log.Printf("answer() response: %s", data)
	user.rank++
}

func getAnswers() []Answer {

	dsn := mysql.Config{
		User:   *dbUser,
		Net:    "tcp",
		Passwd: *dbPass,
		Addr:   *dbHost,
		DBName: *dbName,
		Params: map[string]string{
			"allowNativePasswords": "True",
		},
	}

	db, err := sql.Open("mysql", dsn.FormatDSN())

	if err != nil {
		panic(err.Error())
	}

	err = db.Ping()

	if err != nil {
		panic(err.Error())
	}

	rows, err := db.Query("SELECT rank, answer FROM question ORDER BY rank")

	if err != nil {
		panic(err.Error())
	}
	defer rows.Close()

	var answers []Answer

	for rows.Next() {
		a := Answer{}
		err = rows.Scan(&a.rank, &a.correctAnswer)

		if err != nil {
			panic(err.Error())
		}

		answers = append(answers, a)
	}

	return answers
}

func (user *User) answerFinal(code string, language string) {

	res, status := user.PostJSON("/api/v1/questions/final", map[string]interface{}{
		"text":     code,
		"language": language,
	})

	if status != 200 {
		log.Fatalf("answerFinal() failed: %s\n", res)
	}

	if !res["correct"].(bool) {
		log.Fatalf("answerFinal(): incorrect final answer: %s\n", res)
	}
}

func main() {

	apiServer = flag.String("server", "http://localhost:5000", "API server URL")
	dbHost = flag.String("dbhost", "localhost", "IP or hostname of database server")
	dbUser = flag.String("dbuser", "cc-user", "database username")
	dbPass = flag.String("dbpass", "password", "database password")
	dbName = flag.String("dbname", "code_challenge_local", "database name")
	users := flag.Int("users", 1, "number of users to create")

	flag.Parse()

	res, err := http.Get(*apiServer + "/api/v1/questions/rank")
	if err != nil {
		panic(err.Error())
	}

	data, _ := ioutil.ReadAll(res.Body)
	jsonData := jsonDecode(data)

	currentRank := int(jsonData["rank"].(float64))
	maxRank := int(jsonData["maxRank"].(float64))

	if currentRank != maxRank {
		log.Fatalf("Code Challenge is not at max rank yet. (%d != %d)", currentRank, maxRank)
	}

	answers := getAnswers()

	for i := 0; i < *users; i++ {
		profile := randomdata.GenerateProfile(randomdata.RandomGender)

		jar, _ := cookiejar.New(nil)

		userClient := http.Client{
			Jar: jar,
		}

		u := User{
			Username:         profile.Login.Username,
			StudentFirstName: randomdata.FirstName(randomdata.RandomGender),
			StudentLastName:  randomdata.LastName(),
			StudentEmail:     randomdata.Email(),
			ParentFirstName:  randomdata.FirstName(randomdata.RandomGender),
			ParentLastName:   randomdata.LastName(),
			DOB:              "1994-04-13",
			ParentEmail:      profile.Email,
			Password:         profile.Login.Password + strconv.Itoa(randomdata.Number(10, 100)),
			client:           &userClient,
		}

		u.register()
		u.login()

		for i, ans := range answers {
			if i+1 == len(answers) {
				u.answerFinal(pythonAnswer, "python")
			} else {
				u.answer(ans.correctAnswer)
			}
		}
	}

	log.Println("All data added. Advance CODE_CHALLENGE_START another day to begin voting.")
}
