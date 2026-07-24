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
 *
 * Security: this binary is installed setuid-root (chmod 4755, see the
 * Dockerfile), so its executable bit alone is reachable by ANY caller,
 * not just someone who actually solved level 19 -- the home directory
 * it lives in (bandit19's) being merely non-world-writable was never
 * enough to stop that. Without an explicit caller check, bandit0 (or
 * any other bandit* account) could invoke it directly and jump straight
 * to a bandit20 shell, skipping levels 0-19 entirely. We look up
 * bandit19's UID at runtime (matching however 01-create-users.sh
 * happens to have created that account -- never assume a fixed UID
 * number) and refuse to run unless the REAL uid of the process that
 * invoked us (i.e. whoever is actually logged in and ran this binary)
 * is exactly that. getuid(), not geteuid(): by the time this check
 * runs the effective uid is still 0 (root, from the setuid bit) --
 * it's the real uid that tells us who actually invoked the program. */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pwd.h>

int main(int argc, char **argv) {
    if (argc < 2) {
        return 1;
    }

    struct passwd *caller_pw = getpwnam("bandit19");
    if (!caller_pw) {
        return 1;
    }
    if (getuid() != caller_pw->pw_uid) {
        fprintf(stderr, "This binary may only be run by bandit19.\n");
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
