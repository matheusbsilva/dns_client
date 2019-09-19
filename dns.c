#include <stdlib.h>
#include <stdio.h>
#include <sys/socket.h>


int main(int argc, char *argv[]) {

    int sock_re;

    if((sock_re = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ) {
        perror("socket creation error");
        return 1;
    }

    return 0;
}
