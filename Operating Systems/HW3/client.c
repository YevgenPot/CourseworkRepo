#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <errno.h>
#include <stdlib.h>

struct packet { // declared above main the format of system calls
    int clientid;
    int syscal;
    int nParam;
    int msgSize;
    int value[10];
    char content[10][20];
};

int main(){
    // start sequence of client
    int thisid = getpid();  // get this pid
    char fifostring[20] = "clientfifo";  // initialize client fifo string
    snprintf(fifostring, 20, "client_%d_fifo", thisid);
    printf("Starting client %d\n", thisid);

    printf("Creating %s\n", fifostring);
    if(mkfifo(fifostring, 0777) == -1){  // create client fifo or pass if exist in current directory
        if(errno != EEXIST){
            printf("Error creating fifo file");
            return 1;
        }
    }

    printf("Opening to write...\n");
    int fdwrite = open("serverfifo", O_WRONLY); // connect to server fifo as write
    if (fdwrite== -1){
        return 1;
    }
    printf("Opened.\n");
    //
    // initialize some values allocate memory
    int fdthisfifo = 0;
    struct packet clientcall;
    //
    do{
        printf("type a syscal to request\n");     
        scanf("%d", &clientcall.syscal); // get new syscal
        while( clientcall.syscal != 1 && fdthisfifo == 0 ){ // any syscal that need the client fifo up
            printf("Cannot do this syscal without initial connect. Perform syscal 1.\n");
            printf("type a syscal to request\n");     
            scanf("%d", &clientcall.syscal); // get new syscal
        }

        switch(clientcall.syscal){
            case -1: // terminate
                clientcall.clientid = thisid; // should not change throughout operation
                clientcall.syscal = -1; // 
                clientcall.nParam = 0; // 
                clientcall.msgSize = 0; // 
                write( fdwrite, &clientcall, sizeof(struct packet) );
                break;
            case 0: // revoke this fifo access exit
                clientcall.clientid = thisid; // should not change throughout operation
                clientcall.syscal = 0; // 
                clientcall.nParam = 0; // 
                clientcall.msgSize = 0; // 
                write( fdwrite, &clientcall, sizeof(struct packet) );
                break;
            case 1:
                clientcall.clientid = thisid; // should not change throughout operation
                clientcall.syscal = 1; // user's syscal input, initial syscal MUST BE 1
                clientcall.nParam = 1; // user's num param input, initial syscal 1
                strcpy(clientcall.content[0], fifostring); // puts client fifo name in content
                printf(" opening %s ...\n", clientcall.content[0]); // print check the name is correct
                clientcall.msgSize = sizeof(clientcall.content[0]); // message sizeof

                write( fdwrite, &clientcall, sizeof(struct packet) ); // write to server the syscal 1 packet
                fdthisfifo = open(fifostring, O_RDONLY); // connect to this client fifo read
                //should hang here until server opens this
                printf("Opened this fifo\n");
                break;
            case 2: // num to text
                printf("how many numbers?\n"); // prompt
                scanf("%d", &clientcall.nParam);        // i/o   
                for( int i = 0; i < clientcall.nParam; i++ ){ // loop for each nparam
                    printf("type a number\n");
                    scanf("%d", &clientcall.value[i]); // get int store in packet
                }
                write( fdwrite, &clientcall, sizeof(struct packet) );
                read( fdthisfifo,  &clientcall, sizeof(struct packet) ); // take consumed packet
                printf("\n");
                for( int i = 0; i < clientcall.nParam; i++){ // output the strings for each nparam
                printf("%s\n", clientcall.content[i]);
                }
                break;
            case 3: // text to number
                printf("how many numbers\n");
                scanf("%d", &clientcall.nParam);        // i/o   
                for( int i = 0; i < clientcall.nParam; i++ ){ // loop for each nparam
                    printf("spell a number\n");
                    scanf("%s", &clientcall.content[i][0]); // get int store in packet
                }
                write( fdwrite, &clientcall, sizeof(struct packet) );
                read( fdthisfifo,  &clientcall, sizeof(struct packet) ); // take consumed packet
                printf("\n");                
                for( int i = 0; i < clientcall.nParam; i++){ // output the strings for each nparam
                printf("%d\n", clientcall.value[i]);
                }
                break;
            case 4: // store
                    printf("how many int numbers?\n"); // prompt
                    scanf("%d", &clientcall.nParam);        // i/o   
                        for( int i = 0; i < clientcall.nParam; i++ ){ // loop for each nparam
                            printf("type a number\n"); // get the ints
                            scanf("%d", &clientcall.value[i]); // 
                    }
                    int temp = clientcall.nParam;
                            printf("how many string numbers\n");
                            scanf("%d", &clientcall.nParam);        // i/o   
                        for( int i = 0; i < clientcall.nParam; i++ ){ // loop for each nparam
                            printf("spell a number\n"); // get the strings
                            scanf("%s", &clientcall.content[i][0]); // 
                    }
                    clientcall.nParam = (clientcall.nParam * 10) + temp;
                // end of pooling data
                write( fdwrite , &clientcall, sizeof(struct packet) );
                //
                break;
            case 5: // recall
                write( fdwrite, &clientcall, sizeof(struct packet) );
                read( fdthisfifo, &clientcall, sizeof(struct packet) );
                int intN = clientcall.nParam % 10 ;
                int strN = (clientcall.nParam - intN) / 10;
                printf(" Recalled Ints:\n");
                for( int i = 0; i < intN ; i++){
                    printf("%d\n", clientcall.value[i]);
                }
                printf(" Recalled strings:\n");
                for ( int i = 0; i < strN ; i++ ){
                    printf("%s\n", clientcall.content[i]);
                }

                break;
        }
    }while(clientcall.syscal > 0);

    
    close(fdthisfifo); //
    close(fdwrite); // close fd fifo
    remove(fifostring); // removes clutter fifos
    return 0;
}