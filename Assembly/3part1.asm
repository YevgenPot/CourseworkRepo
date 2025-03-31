.386
.model flat,stdcall
.stack 4096
ExitProcess PROTO, dwExitCode:DWORD

.data
varN DWORD 100

.code
main PROC
mov ECX, varN
mov varN, 0
mov EAX, 0
L:
ADD varN, ECX
LOOP L
mov EAX, varN

INVOKE ExitProcess,0
main ENDP
END main