/* Bandit level 20: SUID binary owned by bandit21, in bandit20's home.
 * Connects OUT to localhost:<argv[1]>, reads one line (the player's own
 * nc listener on that port is expected to send bandit20's current
 * password into this connection), compares it against the known-correct
 * value, and if it matches, writes the next password back over the same
 * connection -- matches the real level's documented behavior.
 *
 * No runtime privilege-drop code here (unlike level 19's helper): this
 * binary's own logic never touches a file gated by bandit21's ownership
 * beyond CONFIG_PATH itself, and it never spawns a shell, so there's no
 * ruid/euid-mismatch pitfall to guard against. The setuid bit + bandit21
 * ownership stays on the FILE regardless, matching the level's real
 * narrative that this is a setuid binary -- a player inspecting it with
 * `ls -la` still sees exactly that.
 *
 * Security: the expected/next passwords are per-team secrets, read from
 * CONFIG_PATH at every run instead of compiled in (see
 * docs/security-audit-status.md) -- a one-time source change,
 * entrypoint.sh regenerates CONFIG_PATH with a fresh per-team value at
 * every container start, no further rebuilds needed per team. CONFIG_PATH
 * is owned bandit21:bandit21, mode 0400 -- readable by this binary only
 * while its effective UID is bandit21 (via the setuid bit), NOT
 * independently readable by bandit20 via a plain `cat`/`find`, preserving
 * the exact same "you must run the binary, not just read a file" security
 * boundary the original compiled-in design had. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define CONFIG_PATH "/etc/bandit21_suconnect.conf"

static int read_config(char *expected, size_t expected_sz, char *next, size_t next_sz) {
    FILE *cf = fopen(CONFIG_PATH, "r");
    if (!cf) {
        fprintf(stderr, "config unavailable\n");
        return -1;
    }
    if (!fgets(expected, expected_sz, cf) || !fgets(next, next_sz, cf)) {
        fclose(cf);
        fprintf(stderr, "config malformed\n");
        return -1;
    }
    fclose(cf);
    expected[strcspn(expected, "\r\n")] = '\0';
    next[strcspn(next, "\r\n")] = '\0';
    return 0;
}

int main(int argc, char **argv) {
    char expected_password[256];
    char next_password[256];

    if (argc < 2) {
        fprintf(stderr, "usage: %s <port>\n", argv[0]);
        return 1;
    }
    if (read_config(expected_password, sizeof(expected_password), next_password, sizeof(next_password)) != 0) {
        return 1;
    }
    int port = atoi(argv[1]);

    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) return 1;

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    inet_pton(AF_INET, "127.0.0.1", &addr.sin_addr);

    if (connect(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        fprintf(stderr, "Could not connect\n");
        return 1;
    }

    char buf[256];
    memset(buf, 0, sizeof(buf));
    ssize_t n = read(sock, buf, sizeof(buf) - 1);
    if (n <= 0) {
        close(sock);
        return 1;
    }
    /* trim trailing newline/CR */
    while (n > 0 && (buf[n - 1] == '\n' || buf[n - 1] == '\r')) {
        buf[--n] = '\0';
    }

    if (strcmp(buf, expected_password) == 0) {
        char reply[258];
        snprintf(reply, sizeof(reply), "%s\n", next_password);
        write(sock, reply, strlen(reply));
    } else {
        write(sock, "Wrong password\n", 16);
    }
    close(sock);
    return 0;
}
