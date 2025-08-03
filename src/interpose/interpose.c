#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdlib.h>

static inline void *gencap(void *base, size_t size) {
    void *ptr;
    asm volatile (".insn r 0x5b, 0x1, 0x40, %0, %1, %2;"
                ".insn r 0x5b, 0x1, 0b1101, x0, %0, x0" : "=r"(ptr)
                                                        : "r"((size_t)base), "r"((size_t)base + size));
    return ptr;
}

static inline void invalidate(void *ptr) {
    asm volatile (".insn r 0x5b, 0b001, 0b0001011, x0, %0, x0" :: "r"(ptr));
}

static inline void *scrub(void *ptr) {
    void *raw_ptr;
    asm volatile (".insn r 0x5b, 0x1, 0x4, %0, %1, x2" : "=r"(raw_ptr) : "r"(ptr));
    return raw_ptr;
}

void *malloc(size_t size) {
    static void *(*real_malloc)(size_t) = NULL;
    if (!real_malloc)
        real_malloc = dlsym(RTLD_NEXT, "malloc");
    return gencap(real_malloc(size), size);
}

void free(void *ptr) {
    static void (*real_free)(void *) = NULL;
    if (!real_free)
        real_free = dlsym(RTLD_NEXT, "free");
    invalidate(ptr);
    real_free(scrub(ptr));
}

void *realloc(void *ptr, size_t size) {
    static void *(*real_realloc)(void *, size_t) = NULL;
    if (!real_realloc)
        real_realloc = dlsym(RTLD_NEXT, "realloc");
    invalidate(ptr);
    return gencap(real_realloc(scrub(ptr), size), size);
}

void *calloc(size_t nmemb, size_t size) {
    static void *(*real_calloc)(size_t, size_t) = NULL;
    if (!real_calloc)
        real_calloc = dlsym(RTLD_NEXT, "calloc");
    return gencap(real_calloc(nmemb, size), nmemb * size);
}

void *reallocarray(void *ptr, size_t nmemb, size_t size) {
    static void *(*real_reallocarray)(void *, size_t, size_t) = NULL;
    if (!real_reallocarray)
        real_reallocarray = dlsym(RTLD_NEXT, "reallocarray");
    invalidate(ptr);
    return gencap(real_reallocarray(scrub(ptr), nmemb, size), nmemb * size);
}
