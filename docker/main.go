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
	"strings"
	"time"
)

var DEBUG = os.Getenv("DEBUG") == "1"

type Response struct {
	Output string `json:"output"`
	Error  string `json:"error"`
}

/**
 * Pass STDIN to the Python interpreter
 */
func execPython(timeout time.Duration, code *string) (stdout string, stderr string) {

	debug("applying seccomp filter for Python")

	ApplySyscallRestrictions()

	debug("building command context with %v timeout", timeout)
	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()

	cmd := exec.CommandContext(ctx, "/usr/bin/python3")
	cmd.Stdin = strings.NewReader(*code)

	var errBuffer bytes.Buffer
	cmd.Stderr = &errBuffer

	debug("executing command ...")
	out, _ := cmd.Output()

	if ctx.Err() == context.DeadlineExceeded {
		debug("command timed out")
		stderr = "command timed out"
		return
	}

	stdout = string(out)
	stderr = errBuffer.String()

	return
}

func execNode(timeout time.Duration, code *string) (stdout string, stderr string) {
	debug("applying seccomp filter for NodeJS")

	ApplySyscallRestrictions()

	debug("building command context with %v timeout", timeout)
	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()

	cmd := exec.CommandContext(ctx, "node")
	cmd.Stdin = strings.NewReader(*code)
	debug("stdin: %s", *code)

	var errBuffer bytes.Buffer
	cmd.Stderr = &errBuffer

	debug("executing command ...")
	out, _ := cmd.Output()

	if ctx.Err() == context.DeadlineExceeded {
		debug("command timed out")
		stderr = "command timed out"
		return
	}

	stdout = string(out)
	stderr = errBuffer.String()

	return
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
	data := string(code)

	if err != nil {
		panic(err.Error())
	}

	var (
		stdout string
		stderr string
	)

	if language == "python" || language == "py" {
		stdout, stderr = execPython(duration, &data)
	} else if language == "javascript" || language == "js" || language == "node" {
		stdout, stderr = execNode(duration, &data)
	}

	r, e := json.Marshal(Response{stdout, stderr})

	if e != nil {
		fmt.Printf(`{"output": "", "error": "unexpected error code output to JSON!"}`)
		return
	}

	fmt.Print(string(r))
}
