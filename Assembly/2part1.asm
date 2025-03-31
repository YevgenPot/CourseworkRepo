; A = (A + B) – (C + D).
include irvine32.inc
.386
.model flat,stdcall
.stack 4096
ExitProcess PROTO, dwExitCode:DWORD
DumpRegs PROTO



.data
varA DWORD 3174
varB DWORD 9825
varC DWORD 4153
varD DWORD 7936

.code
main PROC
mov eax,varA
mov ebx,varB
mov ecx,varC
mov edx,varD
add eax,ebx
add ecx,edx
sub eax,ecx

call DumpRegs

INVOKE ExitProcess,0
main ENDP
END main