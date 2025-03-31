.386
.model flat,stdcall
.stack 4096
ExitProcess PROTO, dwExitCode:DWORD

.data
source BYTE 'STRING' ; string
destination BYTE 6 DUP (?) ; allocated array

.code
main PROC

mov esi, OFFSET source ; \/
add esi, SIZEOF source ; \/
sub esi, TYPE source ; moves sIndex to end of source minus 0
mov edi, OFFSET destination ; moves dIndex to start of destination
mov ECX, LENGTHOF source ; sets ECX to length of source array

L1:
mov AL, [esi]
mov [edi], AL
SUB esi, TYPE source
ADD edi, TYPE source
LOOP L1 ; uses AL to move sIndex element to dIndex element, moves sIndex down and dIndex up by data type of source

INVOKE ExitProcess,0
main ENDP
END main