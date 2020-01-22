#!/usr/bin/python3

import json
import os
import sys
from subprocess import Popen, PIPE
from typing import Tuple

from pyduktape import DuktapeContext

CODE_FOLDER = "/mnt/code/"

CLIOutput = Tuple[str, str]  # stdout/stderr


def echo(output="", error="") -> None:
    print(json.dumps({
        "output": output,
        "error": error
    }))


def exec_python(code: str) -> CLIOutput:
    p = Popen("/usr/bin/python3", stdin=PIPE, stderr=PIPE, stdout=PIPE)
    stdout, stderr = p.communicate(code.encode("utf8"))

    return stdout.decode("utf8"), stderr.decode("utf8")


def exec_js(code: str) -> CLIOutput:
    ctx = DuktapeContext()

    output = ""
    error = ""

    try:
        output = ctx.eval_js(code)
    except Exception as e:
        error = str(e)

    return output, error


def main() -> int:
    language = os.getenv("LANGUAGE")
    filename = os.getenv("CODEFILE")
    code = ""

    with open(os.path.join(CODE_FOLDER, filename), "r") as contents:
        code = contents.read()

    stdout, stderr = "", ""

    if language not in ("python", "js"):
        echo(error=f"unsupported language {language!r}")
        return -1

    if language == "python":
        stdout, stderr = exec_python(code)

    elif language == "js":
        stdout, stderr = exec_js(code)

    echo(stdout, stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
