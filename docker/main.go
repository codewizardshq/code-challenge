// LANGUAGE=py CODEFILE=test.py strace -fqxy -a0 -s32 ./main

package main

import (
	"bytes"
	"context"
	"encoding/json"
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

func main() {
	debug("main go code started")
	language := os.Getenv("LANGUAGE")
	codeFolder := os.Getenv("CODEFOLDER")

	if codeFolder == "" {
		codeFolder = "/mnt/code"
	}

	filename := path.Join(codeFolder, os.Getenv("CODEFILE"))
	timeoutEnv := os.Getenv("TIMEOUT")

	if timeoutEnv == "" {
		timeoutEnv = "5"
	}

	timeout, err := strconv.Atoi(timeoutEnv)
	duration := time.Duration(timeout) * time.Second

	if err != nil {
		panic(err.Error())
	}

	debug("reading file: %s", filename)
	code, err := ioutil.ReadFile(filename)
	// data := string(code)

	if err != nil {
		panic(err.Error())
	}

	var (
		interpreter string
		response    *Response
	)

	switch language {
	case "python":
	case "py":
		interpreter = "/usr/bin/python3"
	case "javascript":
	case "js":
	case "node":
		interpreter = "node"
	default:
		response = &Response{Error: "unrecognized language: " + language}
		fmt.Print(response.toJSON())
		return
	}

	response = execSandbox(interpreter, duration, code)

	fmt.Print(response.toJSON())
}
