/* Bandit level 19: setuid-root binary in bandit19's home that drops
 * privilege down to bandit20 and runs the given command.
 *
 * Deliberately setuid ROOT, not setuid bandit20 directly -- confirmed by
 * live testing that the latter doesn't actually work for this purpose:
 * a process that becomes euid=bandit20 purely via the file's setuid bit
 * (starting from an unprivileged real UID) has no CAP_SETUID, so it
 * cannot fully consolidate real+effective+saved UID via its own
 * setuid() call. system()'s spawned /bin/sh then sees ruid != euid and
 * drops back to the real (unprivileged) UID as its own safety measure
 * before the requested command ever runs -- "Permission denied" on
 * anything actually gated by bandit20's ownership, reproduced and
 * confirmed via a standalone diagnostic before settling on this fix.
 * Starting as root (which DOES have CAP_SETUID) and dropping down
 * cleanly avoids the mismatch entirely: the spawned shell sees a
 * consistent real=effective=bandit20 UID, exactly like a normal login.
 */
#include <stdlib.h>
#include <unistd.h>
#include <pwd.h>

int main(int argc, char **argv) {
    if (argc < 2) {
        return 1;
    }
    struct passwd *pw = getpwnam("bandit20");
    if (!pw) {
        return 1;
    }
    if (setgid(pw->pw_gid) != 0) {
        return 1;
    }
    if (setuid(pw->pw_uid) != 0) {
        return 1;
    }
    return system(argv[1]);
}
