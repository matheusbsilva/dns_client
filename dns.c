#include <stdlib.h>
#include <stdio.h>
#include <sys/socket.h>

struct dns_header {
    unsigned int id;

    unsigned int qr :1;
    unsigned int opcode :4;
    unsigned int auth_answer :1;
    unsigned int truncation :1;
    unsigned int recursion_desired :1;
    unsigned int recursion_available :1;
    unsigned int z;
    unsigned int rcode :4;

    unsigned int qdcount;
    unsigned int ancount;
    unsigned int nscount;
    unsigned int arcount;
};

int main(int argc, char *argv[]) {

    int sock_re;

    if((sock_re = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ) {
        perror("socket creation error");
        return 1;
    }

    return 0;
}
