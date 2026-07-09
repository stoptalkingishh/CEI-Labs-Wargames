/* Krypton level 2: Caesar cipher with an unknown shift. Reads the shift
 * from a *binary* keyfile (a single opaque byte, not human-readable
 * digits -- `cat keyfile.dat` shouldn't just hand you the answer) in the
 * CURRENT directory, then Caesar-shifts stdin to stdout. Matches the
 * real lesson: symlink krypton2's keyfile.dat into a scratch dir, feed
 * this binary a known plaintext (e.g. all 'A's), and read the shift off
 * the output instead of ever seeing it directly. */
#include <stdio.h>
#include <ctype.h>

int main(void) {
    FILE *kf = fopen("keyfile.dat", "rb");
    if (!kf) {
        fprintf(stderr, "encrypt: keyfile.dat not found in current directory\n");
        return 1;
    }
    int b = fgetc(kf);
    fclose(kf);
    if (b == EOF) {
        fprintf(stderr, "encrypt: keyfile.dat is empty\n");
        return 1;
    }
    int shift = ((unsigned char)b) % 26;

    int c;
    while ((c = getchar()) != EOF) {
        if (isupper(c)) {
            c = 'A' + (c - 'A' + shift) % 26;
        } else if (islower(c)) {
            c = 'a' + (c - 'a' + shift) % 26;
        }
        putchar(c);
    }
    return 0;
}
