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

// sub function, take a int and return english sting equivalent
const char* intToString(int num){  //
    const char* string;
    switch(num){
        case 0:
            string = "zero";
            return string;
            break;
        case 1:
            string = "one";
            return string;
            break;
        case 2:
            string = "two";
            return string;
            break;
        case 3:
            string = "three";
            return string;
            break;
        case 4:
            string = "four";
            return string;
            break;
        case 5:
            string = "five";
            return string;
            break;
        case 6:
            string = "six";
            return string;
            break;
        case 7:
            string = "seven";
            return string;
            break;
        case 8:
            string = "eight";
            return string;
            break;
        case 9:
            string = "nine";
            return string;
            break;
    }
}
// end of sub function int to string
///
// sub function, take english sting and return int equivalent
int stringToInt( char string[] ){
    int num;
    switch(string[0]){ // word to int switch
        case (122): // ascii z 
            num = 0;
            return num;
            break;
        case (111):   // ascii t then if ascii w or ascii h
            num = 1;
            return num;
            break;
        case (116):
            if(string[1] == 119){
                num = 2;
                return num;
            } else if(string[1] == 104){
                num = 3;
                return num;
            }
            break;
        case (102):
            if(string[1] == 111){
                num = 4;
                return num;
            } else if(string[1] == 105){
                num = 5;
                return num;
            }
            break;
        case (115):
            if(string[1] == 105){
                num = 6;
                return num;
            } else if(string[1] == 101){
                num = 7;
                return num;
            }
            break;
        case (101):
            num = 8;
            return num;
            break;
        case (110):
            num = 9;
            return num;
            break;
    }
}
// end of sub function string to int
///
int main(){
    // start sequence for server main
    printf("Starting Server...\n");

    
    if(mkfifo("serverfifo", 0777) == -1){  // create server fifo or pass if exists
        if(errno != EEXIST){
            printf("Error creating fifo file");
            return 1;
        }
    }

    printf("Opening to read...\n");
    int fdread = open("serverfifo", O_RDONLY); // opens file in mode read, returns file desc
    if (fdread == -1){
        return 1;
    }
    printf("Opened server reading.\n");
    // 
    //
    struct packet nullpacket; // empty packet for reinitialization
    struct packet recievedClient; // initialize read packet space
    int serverUp = 1; // used to turn off server
    int fdclient [10]; // a table of current client fifo's
    int fdclientInx;
    int clientIds[10];
    struct packet storedPacket[10]; // an array of saved packets
    char packetline[10][20];
    int linefront = 0;
    int lineback = 0;
    //
    do{
        read( fdread, &recievedClient, sizeof(struct packet) ); // read the current clients write packet
        printf(" Client PID: %d", recievedClient.clientid);
        printf(", Syscal %d\n", recievedClient.syscal);

        for(int i = 0 ; i < 10 ; i++){ // find if packet's client is a saved client
            if( clientIds[i] == recievedClient.clientid ){
                fdclientInx = i;
            }
        }

        switch(recievedClient.syscal){
            case -1:
                close(fdclient[fdclientInx]); 
                fdclient[fdclientInx]= 0;
                serverUp = 0;
                printf("Terminating...\n");
                break;
            case 0:
                close(fdclient[fdclientInx]); 
                recievedClient = nullpacket;////
                storedPacket[fdclientInx] = nullpacket;
                printf(" Goodbye\n");
                if( packetline[linefront] != 0 ){
                fdclient[fdclientInx] = open( packetline[linefront], O_WRONLY );///pull from line
                printf("Now writing on %s\n", packetline[linefront]);
                linefront++;
                }// when current client leaves, pull the next pending client
                break;
            case 1: // open client fifo
                    for(int i = 0 ; i < 10 ; i++){
                        if ( fdclient[i] == 0 ){ // find a index that is empty put fifo in there
                            fdclient[i] = open(recievedClient.content[0], O_WRONLY);
                            clientIds[i] = recievedClient.clientid  ;
                            printf("saved client %s\n", recievedClient.content[0]);
                            break;
                        }
                        if( i == 9 ){ // this is last index and its full
                            strcpy( packetline[lineback] , recievedClient.content[0] );///copy that fifo info and push it
                            printf("%s pushed to line \n", packetline[lineback]);
                            lineback++;
                        }
                    }
                break;
            case 2: // process number return string
                for( int i = 0; i < recievedClient.nParam; i++ ){
                    strcpy( recievedClient.content[i], intToString(recievedClient.value[i]) );
                }
                write( fdclient[fdclientInx], &recievedClient, sizeof(struct packet) );
                break;
            case 3:
                for ( int i = 0; i < recievedClient.nParam; i++){
                    recievedClient.value[i] = stringToInt(recievedClient.content[i]);
                }
                write ( fdclient[fdclientInx], &recievedClient, sizeof(struct packet) );
                break;
            case 4: // storage
                storedPacket[fdclientInx] = recievedClient;
                break;
            case 5: // retrieve 
                write( fdclient[fdclientInx], &(storedPacket[fdclientInx]), sizeof(struct packet) );
                storedPacket[fdclientInx] = nullpacket;
                break;
        }
    }while(serverUp);


    close(fdread); // close fd serverfifo
}