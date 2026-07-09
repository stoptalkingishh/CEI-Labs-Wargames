/* Krypton level 6: additive stream cipher keyed by a Linear-Feedback
 * Shift Register whose output repeats every 30 symbols. Ciphertext[i] =
 * (plaintext[i] + keystream[i mod 30]) mod 26 over uppercase letters
 * (lowercase handled the same way; non-letters pass through and don't
 * advance the keystream index). Encrypting a long run of 'A's (== 0)
 * directly exposes the keystream itself, which is the intended lesson:
 * recover all 30 keystream values that way, then subtract them from the
 * real ciphertext to recover the plaintext. */
#include <stdio.h>
#include <ctype.h>

static const int KEYSTREAM[30] = {
    13, 4, 0, 19, 12, 12, 10, 8, 5, 16, 15, 0, 15, 5, 4, 18,
    24, 21, 15, 3, 0, 4, 16, 4, 5, 10, 3, 5, 22, 7
};

int main(void) {
    int c;
    int i = 0;
    while ((c = getchar()) != EOF) {
        if (isupper(c)) {
            c = 'A' + (c - 'A' + KEYSTREAM[i % 30]) % 26;
            i++;
        } else if (islower(c)) {
            c = 'a' + (c - 'a' + KEYSTREAM[i % 30]) % 26;
            i++;
        }
        putchar(c);
    }
    return 0;
}
