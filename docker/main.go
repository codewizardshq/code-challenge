// LANGUAGE=py CODEFILE=test.py strace -fqxy -a0 -s32 ./main

package main

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"os/exec"
	"path"
	"strconv"
	"time"
)

var DEBUG = os.Getenv("DEBUG") == "1"

type Response struct {
	Output        string `json:"output"`
	Error         string `json:"error"`
	ExecutionTime int64  `json:"time"`
}

func (r Response) toJSON() string {
	data, _ := json.Marshal(r)
	return string(data)
}

func (r Response) Done() {
	fmt.Print(r.toJSON())
}

func execSandbox(interpreter string, timeout time.Duration, code []byte) *Response {
	res := Response{}
	ApplySyscallRestrictions()

	debug("building command context with %v timeout", timeout)
	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()

	cmd := exec.CommandContext(ctx, interpreter)
	cmd.Stdin = bytes.NewReader(code)

	var errBuffer bytes.Buffer
	cmd.Stderr = &errBuffer

	debug("executing command ...")
	start := time.Now()
	out, _ := cmd.Output()
	elapsed := time.Since(start)

	res.ExecutionTime = elapsed.Milliseconds()

	if ctx.Err() == context.DeadlineExceeded {
		debug("command timed out")
		res.Error = "command timed out"
	}

	res.Output = string(out)
	res.Error = errBuffer.String()

	return &res
}

func debug(msg string, args ...interface{}) {
	if DEBUG {
		log.Println(fmt.Sprintf(msg, args...))
	}
}

func getenv(key string, defaultValue string) string {
	v := os.Getenv(key)
	if v == "" {
		return defaultValue
	}
	return v
}

func lookupInterpreter(language string) (string, error) {
	var interpreter string
	var err error

	switch language {
	case "python":
	case "py":
		interpreter = "/usr/bin/python3"
	case "javascript":
	case "js":
	case "node":
		interpreter = "node"
	case "":
		err = errors.New("language not specified")
	default:
		err = errors.New("unrecognized language: " + language)
	}

	return interpreter, err
}

func main() {
	var (
		interpreter string
		response    *Response
		filename    string
		timeout     int
		code        []byte
	)

	debug("main go code started")

	filename = path.Join(getenv("CODEFOLDER", "/mnt/code"), os.Getenv("CODEFILE"))
	timeout, err := strconv.Atoi(getenv("TIMEOUT", "5"))

	if err != nil {
		panic(err.Error())
	}

	debug("reading file: %s", filename)
	code, err = ioutil.ReadFile(filename)

	if err != nil {
		panic(err.Error())
	}

	interpreter, err = lookupInterpreter(os.Getenv("LANGUAGE"))

	if err != nil {
		response = &Response{Error: err.Error()}
		response.Done()
		return
	}

	response = execSandbox(interpreter, time.Duration(timeout)*time.Second, code)
	response.Done()
}
