

#ifndef TRYCRYPT_CRYPTOOL_H
#define TRYCRYPT_CRYPTOOL_H

#include <cstdio>
#include "sodium.h"
#include <cstring>

#define CHUNK_SIZE 4096
#ifdef __cplusplus
extern "C" {
#endif
int
encrypt(const char *target_file, const char *source_file, const char *PASSWORD);

int
decrypt(const char *target_file, const char *source_file, const char *PASSWORD);
#ifdef __cplusplus
}
#endif
#endif //TRYCRYPT_CRYPTOOL_H
