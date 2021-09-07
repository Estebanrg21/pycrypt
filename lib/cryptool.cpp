

#include "cryptool.h"

 int
encrypt(const char *target_file, const char *source_file, const char *const PASSWORD) {
    try {
        unsigned char buf_in[CHUNK_SIZE];
        unsigned char buf_out[CHUNK_SIZE + crypto_secretstream_xchacha20poly1305_ABYTES];
        unsigned char header[crypto_secretstream_xchacha20poly1305_HEADERBYTES];
        crypto_secretstream_xchacha20poly1305_state st;
        FILE *fp_t, *fp_s;
        unsigned long long out_len;
        size_t rlen;
        int eof;
        unsigned char tag;

        fp_s = fopen(source_file, "rb");
        fp_t = fopen(target_file, "wb");

        unsigned long long opslimit = crypto_pwhash_argon2id_OPSLIMIT_MIN;
        unsigned long long memlimit = crypto_pwhash_argon2id_MEMLIMIT_MIN;
        int alg = crypto_pwhash_ALG_DEFAULT;
        unsigned char salt[crypto_pwhash_SALTBYTES];
        randombytes_buf(salt, sizeof salt);
        unsigned char key[crypto_secretstream_xchacha20poly1305_KEYBYTES];
        fwrite(&opslimit, sizeof(unsigned long long), 1, fp_t);
        fwrite(&memlimit, sizeof(unsigned long long), 1, fp_t);
        fwrite(&alg, sizeof(int), 1, fp_t);
        fwrite(&salt, sizeof salt, 1, fp_t);
        crypto_pwhash(key, sizeof key, PASSWORD, strlen(PASSWORD), salt,
                      opslimit, memlimit,
                      alg);


        crypto_secretstream_xchacha20poly1305_init_push(&st, header, key);
        fwrite(header, 1, sizeof header, fp_t);
        do {
            rlen = fread(buf_in, 1, sizeof buf_in, fp_s);
            eof = feof(fp_s);
            tag = eof ? crypto_secretstream_xchacha20poly1305_TAG_FINAL : 0;
            crypto_secretstream_xchacha20poly1305_push(&st, buf_out, &out_len, buf_in, rlen,
                                                       NULL, 0, tag);
            fwrite(buf_out, 1, (size_t) out_len, fp_t);
        } while (!eof);
        fclose(fp_t);
        fclose(fp_s);
        return 0;
    } catch (...) {
        return -1;
    }
}

int
decrypt(const char *target_file, const char *source_file, const char *const PASSWORD) {
    try {
        unsigned char buf_in[CHUNK_SIZE + crypto_secretstream_xchacha20poly1305_ABYTES];
        unsigned char buf_out[CHUNK_SIZE];
        unsigned char header[crypto_secretstream_xchacha20poly1305_HEADERBYTES];
        crypto_secretstream_xchacha20poly1305_state st;
        FILE *fp_t, *fp_s;
        unsigned long long out_len;
        size_t rlen;
        int eof;
        int ret = 0;
        unsigned char tag;

        fp_s = fopen(source_file, "rb");
        fp_t = fopen(target_file, "wb");


        unsigned long long opslimit;
        unsigned long long memlimit;
        int alg;
        unsigned char salt[crypto_pwhash_SALTBYTES];
        unsigned char key[crypto_secretstream_xchacha20poly1305_KEYBYTES];
        fread(&opslimit, sizeof(unsigned long long), 1, fp_s);
        fread(&memlimit, sizeof(unsigned long long), 1, fp_s);
        fread(&alg, sizeof(int), 1, fp_s);
        fread(&salt, sizeof salt, 1, fp_s);
        crypto_pwhash(key, sizeof key, PASSWORD, strlen(PASSWORD), salt,
                      opslimit, memlimit,
                      alg);


        fread(header, 1, sizeof header, fp_s);
        if (crypto_secretstream_xchacha20poly1305_init_pull(&st, header, key) != 0) {
            ret = -1; /* incomplete header */
        }
        do {
            rlen = fread(buf_in, 1, sizeof buf_in, fp_s);
            eof = feof(fp_s);
            if (crypto_secretstream_xchacha20poly1305_pull(&st, buf_out, &out_len, &tag,
                                                           buf_in, rlen, NULL, 0) != 0) {
                ret = -1; /* corrupted chunk */
            }
            if (tag == crypto_secretstream_xchacha20poly1305_TAG_FINAL && !eof) {
                ret = -1; /* premature end (end of file reached before the end of the stream) */
            }
            fwrite(buf_out, 1, (size_t) out_len, fp_t);
        } while (!eof && ret == 0);
        fclose(fp_t);
        fclose(fp_s);
        return ret;
    } catch (...) {
        return -1;
    }
}