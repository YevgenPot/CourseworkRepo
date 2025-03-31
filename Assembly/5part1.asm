INCLUDE Irvine32.inc

.386
.model flat,stdcall
.stack 4096
ExitProcess PROTO, dwExitCode:DWORD

.data
string BYTE "this is a string",0
colors DWORD white,red,yellow,green

.code
main PROC

mov ECX, 4 ; set counter

mov ESI, OFFSET colors ; move each color value to stack
mov EBX, [esi]
push EBX
mov EBX, [esi+4]
push EBX
mov EBX, [esi+8]
push EBX
mov EBX, [esi+12]
push EBX

L:
pop EBX	; take color value out of stack, use it to set color and write
mov EAX, EBX
call SetTextColor
mov EDX, OFFSET string
call WriteString
call Crlf
LOOP L

INVOKE ExitProcess,0
main ENDP
END main