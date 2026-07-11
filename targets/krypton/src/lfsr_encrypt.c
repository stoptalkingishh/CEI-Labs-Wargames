/* Krypton level 6: additive stream cipher keyed by a Linear-Feedback
 * Shift Register whose output repeats every 30 symbols. Ciphertext[i] =
 * (plaintext[i] + keystream[i mod 30]) mod 26 over uppercase letters
 * (lowercase handled the same way; non-letters pass through and don't
 * advance the keystream index). Encrypting a long run of 'A's (== 0)
 * directly exposes the keystream itself, which is the intended lesson:
 * recover all 30 keystream values that way, then subtract them from the
 * real ciphertext to recover the plaintext.
 *
 * The keystream is read from keystream.dat (30 raw bytes, each taken mod
 * 26) in the CURRENT directory at every run, rather than compiled in --
 * this is what lets entrypoint.sh generate a fresh per-team keystream at
 * container start instead of every team sharing the same one baked into
 * the image (see docs/security-audit-status.md). Same runtime-file
 * pattern as krypton2's encrypt binary and its keyfile.dat. */
#include <stdio.h>
#include <ctype.h>

int main(void) {
    int keystream[30];
    unsigned char buf[30];

    FILE *kf = fopen("keystream.dat", "rb");
    if (!kf) {
        fprintf(stderr, "encrypt: keystream.dat not found in current directory\n");
        return 1;
    }
    size_t n = fread(buf, 1, 30, kf);
    fclose(kf);
    if (n != 30) {
        fprintf(stderr, "encrypt: keystream.dat must be exactly 30 bytes\n");
        return 1;
    }
    for (int j = 0; j < 30; j++) {
        keystream[j] = buf[j] % 26;
    }

    int c;
    int i = 0;
    while ((c = getchar()) != EOF) {
        if (isupper(c)) {
            c = 'A' + (c - 'A' + keystream[i % 30]) % 26;
            i++;
        } else if (islower(c)) {
            c = 'a' + (c - 'a' + keystream[i % 30]) % 26;
            i++;
        }
        putchar(c);
    }
    return 0;
}
