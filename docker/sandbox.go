package main

import (
	"fmt"
	libseccomp "github.com/seccomp/libseccomp-golang"
	"syscall"
)

func ApplySyscallRestrictions() {
	// syscalls go here
	var syscalls = []string{"read", "write", "close", "mmap", "munmap",
		"rt_sigaction", "rt_sigprocmask", "clone", "execve", "sigaltstack",
		"arch_prctl", "gettid", "futex", "sched_getaffinity", "epoll_ctl",
		"openat", "newfstatat", "readlinkat", "pselect6", "epoll_pwait",
		"epoll_create1", "exit_group", "pipe2", "brk", "exit",
		"dup2", "writev", "fstat", "mprotect", "fcntl", "open", "sched_yield",
		"pread64", "getpid", "rt_sigsuspend", "stat", "rt_sigreturn",
		"getrandom", "sysinfo", "lseek", "getdents64", "ioctl",
		"membarrier", "waitid", "wait4", "readlink", "nanosleep",
		"getgid", "getegid", "getuid", "geteuid", "dup", "clock_gettime",
		"access", "getcwd", "set_tid_address", "kill", "tgkill"}

	whiteList(syscalls)
}

// Load the seccomp whitelist.
func whiteList(syscalls []string) {

	filter, err := libseccomp.NewFilter(
		libseccomp.ActErrno.SetReturnCode(int16(syscall.EPERM)))

	if err != nil {
		fmt.Printf("Error creating filter: %s\n", err)
	}
	for _, element := range syscalls {
		// fmt.Printf("[+] Whitelisting: %s\n", element)
		syscallID, err := libseccomp.GetSyscallFromName(element)
		if err != nil {
			panic(err)
		}
		filter.AddRule(syscallID, libseccomp.ActAllow)
	}
	filter.Load()
}
