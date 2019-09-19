#include <stdlib.h>
#include <stdio.h>
#include <sys/socket.h>
#include<arpa/inet.h>
#include<netinet/in.h>

struct header {
    unsigned short id;

    unsigned char qr :1;
    unsigned char opcode :4;
    unsigned char auth_answer :1;
    unsigned char truncation :1;
    unsigned char recursion_desired :1;
    unsigned char recursion_available :1;
    unsigned char z;
    unsigned char rcode :4;

    unsigned short qdcount;
    unsigned short ancount;
    unsigned short nscount;
    unsigned short arcount;
};

struct question {
    
};

int main(int argc, char *argv[]) {

    char msg[] = {
        0 ,  42,                           // HEADER: ID
        0 ,  0 ,                           // HEADER: Various flags
        0 ,  1 ,                           // HEADER: QDCOUNT
        0 ,  0 ,                           // HEADER: ANCOUNT
        0 ,  0 ,                           // HEADER: NSCOUNT
        0 ,  0 ,                           // HEADER: ARCOUNT
        3 , 'w', 'w', 'w',                 // QUESTION: QNAME: label 1
        6 , 'g', 'o', 'o', 'g', 'l', 'e',  // QUESTION: QNAME: label 2
        3 , 'c', 'o', 'm',                 // QUESTION: QNAME: label 3
        0 ,                                // QUESTION: QNAME: null label
        0 ,  1 ,                           // QUESTION: QTYPE
        0 ,  1                             // QUESTION: QCLASS
    };

    struct sockaddr_in dest;

    dest.sin_family = AF_INET;
    dest.sin_port = htons(53);
    dest.sin_addr.s_addr = inet_addr("8.8.8.8");

    int sock_re;

    if((sock_re = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ) {
        perror("socket creation error");
        return 1;
    }

    if(sendto(sock_re, (void *)msg, sizeof(msg), 0, (struct sockaddr*)&dest, sizeof(dest)) < 0) {
        perror("sendto failed");
        return 1;
    }

    return 0;
}
