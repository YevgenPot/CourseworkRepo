INCLUDE Irvine32.inc

.386
.model flat,stdcall
.stack 4096
ExitProcess PROTO, dwExitCode:DWORD

.data

IntOne SDWORD ? ; 
IntTwo SDWORD ?
Oprt SDWORD ?

.code
main PROC

;user enters 2 ints unsigned
;user enters opperation 1-addition 2-subtraction 3- multipl 4-divison
call ReadInt ;stores in EAX value
mov IntOne, EAX ; store value from EAX to var
call ReadInt
mov IntTwo, EAX
call ReadInt
mov Oprt, EAX

CMP Oprt, 1 ; is this addition
JNZ TrySub ; try next operation if no
mov EAX, IntOne
ADD EAX, IntTwo
mov IntOne, EAX
JMP Exitt

TrySub:
CMP Oprt, 2 ; is this subtraction
JNZ TryMul ; 
mov EAX, IntOne
SUB EAX, IntTwo
mov IntOne, EAX
JMP Exitt

TryMul:
CMP Oprt, 3 ; is this multiplication
JNZ TryDiv ; 
mov EAX, IntTwo ; move int to eax for multiplication division
IMUL IntOne ; answer is in EAX lower, EDX upper
JMP Exitt

TryDiv:
CMP Oprt, 4 ;
JNZ Exitt ; exit if not an operation
mov EAX, IntOne ; move int to eax for multiplication division
TEST EAX, 10000000000000000000000000000000b ; what sign is eax
JZ Pos ; positive? jump to positive set
mov EDX, 11111111111111111111111111111111b ; sets edx sign extend if eax is negative
JMP DoDiv ; set then do the division
Pos:
mov EDX, 0 ; sets edx for division if eax is positive
DoDiv:
IDIV IntTwo ; 

Exitt:
CMP Oprt, 2
JG Write34 ; we did not do add/sub, jump to mul/div
mov EAX, IntOne ; simple move to eax and write
call WriteInt
JMP Endd

Write34: ; homework stated we could use the repeated addition PROC, which overflows if answer exceeds EAX capacity, so user output cannot exceed EAX capacity
CMP Oprt, 4 ; 
JG Endd ; we did not do mul/div, skip write
;push EAX ; save current EAX to stack, this should be the lower portion of mul/div answer
;mov EAX, EDX ; move to eax/write register the upper portion of mul/div answer
;call WriteInt
;pop EAX ; mov saved lower portion of mul/div answer
call WriteInt

Endd:

INVOKE ExitProcess,0
main ENDP
END main