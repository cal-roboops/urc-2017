//
// Server.h - Version 2
// CPP Project
//
// Created by Mitchell Oleson on 2/8/2016
//
// Written for Debian Linux
//

#define BACKLOG 3
#define DEFAULT_BUFLEN 512

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <netdb.h>
#include <unistd.h>
#include <sys/socket.h>

// Server Class
class Server {
	private:
	    // Private Variables
	    char* listening_port;

	    int status;
	    int iResult;
	    int ServerSocket;
	    socklen_t addr_size;
	    struct addrinfo host_info;
	    struct addrinfo *host_info_list;
	    struct sockaddr_storage client_addr;

	    int iSendResult;
 	    int iReceiveResult;
	    static const int recvbuflen = DEFAULT_BUFLEN;
	    static const int sendbuflen = DEFAULT_BUFLEN;

	    // Private Methods
	    int server_socket();
	    int server_connect();

	public:
	    // Public Variables
	    char recvbuf[DEFAULT_BUFLEN];
	    char msgbuf[DEFAULT_BUFLEN];

	    // Public Methods
	    Server(char* port);
	    ~Server();
	    int server_receive();
	    int server_send(const char* msg);
};