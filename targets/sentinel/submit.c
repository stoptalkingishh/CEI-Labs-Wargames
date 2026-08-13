#include <stdlib.h>
#include <pwd.h>
#include <unistd.h>

int main(void) {
    struct passwd *caller = getpwuid(getuid());
    if (caller == NULL) {
        return 126;
    }
    char *const argv[] = {"/usr/bin/python3", "-Es", "/opt/sentinel/answer_service.py", caller->pw_name, NULL};
    char *const envp[] = {"PATH=/usr/bin:/bin", "LANG=C", NULL};

    if (setgid(0) != 0 || setuid(0) != 0) {
        return 126;
    }
    execve(argv[0], argv, envp);
    return 127;
}
