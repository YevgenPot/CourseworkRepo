INCLUDE Irvine32.inc

.386
.model flat,stdcall
.stack 4096
ExitProcess PROTO, dwExitCode:DWORD

.data

varR SDWORD ? ; random var

.code
main PROC

call ReadInt ; stores user lower bound in EAX
mov EBX, EAX ; moves lower bound to EBX
call ReadInt; stores user upper bound cannot be negative for the use of RandomRange
mov EDX, EAX ; moves upper bound to EDX
call Crlf

mov ECX, 10

call Randomize ; randomizes seed 

L1:

call BetterRandomRange

LOOP L1

JMP Endd

BetterRandomRange PROC

Redo:
mov EAX, EDX ; refresh upper bound for RandomRange
call RandomRange ; returns ranged random number to EAX
mov varR, EAX

call Random32 ; returns some random number to EAX
TEST AL, 0001b ; is some random number odd?
JNZ Final ; if yes, skip try to use lower bound as range

LowerRange:
TEST EBX, 10000000000000000000000000000000b ; is lower bound negative
JZ Final ; if positive, skip to final step  

mov varR, EBX ; lower bound is negative, temp move to varR
NEG varR ; make lower bound positive
mov EAX, varR 
call RandomRange ; using lower bound magnitude
mov varR, EAX
NEG varR ; make positive into negative


Final:
CMP varR, EBX ; is ranged random number within lower bound
JL Redo

mov EAX, varR ; value passes lower bound check, move to EAX for WriteInt

call WriteInt ; writes random var
call Crlf
RET

BetterRandomRange ENDP

Endd:

INVOKE ExitProcess,0
main ENDP
END main