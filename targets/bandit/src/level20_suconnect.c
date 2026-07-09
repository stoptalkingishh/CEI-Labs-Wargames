/* Bandit level 20: SUID binary owned by bandit21, in bandit20's home.
 * Connects OUT to localhost:<argv[1]>, reads one line (the player's own
 * nc listener on that port is expected to send bandit20's current
 * password into this connection), compares it against the known-correct
 * value, and if it matches, writes the next password back over the same
 * connection -- matches the real level's documented behavior.
 *
 * No runtime privilege-drop code here (unlike level 19's helper): this
 * binary's own logic never touches a file gated by bandit21's ownership
 * (the expected/next values are baked in at compile time, not read from
 * /etc/bandit_pass/ -- see the comment below), and it never spawns a
 * shell, so there's no ruid/euid-mismatch pitfall to guard against.
 * The setuid bit + bandit21 ownership stays on the FILE regardless,
 * matching the level's real narrative that this is a setuid binary --
 * a player inspecting it with `ls -la` still sees exactly that. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

/* Kept here rather than reading /etc/bandit_pass/bandit20 at runtime --
 * baking the expected value in directly avoids adding a bandit21-
 * readable password file that would itself leak the answer via
 * `find`/`cat` before the binary is even used, which would break the
 * level. */
#define EXPECTED_PASSWORD "GbKksEFF4yrVs6il55v6gwY5aVje5f0j"
#define NEXT_PASSWORD "gE269g2h3mw3pwgrj0LuIpTpNcfS1KMc"

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "usage: %s <port>\n", argv[0]);
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

    if (strcmp(buf, EXPECTED_PASSWORD) == 0) {
        write(sock, NEXT_PASSWORD "\n", strlen(NEXT_PASSWORD "\n"));
    } else {
        write(sock, "Wrong password\n", 16);
    }
    close(sock);
    return 0;
}
