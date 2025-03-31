; A = (A + B) – (C + D).
include irvine32.inc
.386
.model flat,stdcall
.stack 4096
ExitProcess PROTO, dwExitCode:DWORD
DumpRegs PROTO



.data
.code
main PROC
mov eax,0
mov al,0FFh
add ax,32511
inc ax

call DumpRegs

INVOKE ExitProcess,0
main ENDP
END main