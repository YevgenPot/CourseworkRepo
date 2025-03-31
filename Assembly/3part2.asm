.386
.model flat,stdcall
.stack 4096
ExitProcess PROTO, dwExitCode:DWORD

.data
num1 WORD 123 ; the number we will use for addition
num2 WORD 456 ; the amount of times we perform addition, cannot be 0

.code
main PROC

movSX EBX, num1 ; sets EBX to num1
movSX ECX, num2 ; sets ECX to num2
mov EAX, 0 ; initialize EAX with 0

L:
ADD EAX, EBX 
LOOP L ; adds num1 to EAX by num2 times

INVOKE ExitProcess,0
main ENDP
END main