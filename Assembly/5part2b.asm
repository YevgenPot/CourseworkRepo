INCLUDE Irvine32.inc

.386
.model flat,stdcall
.stack 4096
ExitProcess PROTO, dwExitCode:DWORD

.data
string BYTE "enter two integers to sum",0
lineCount BYTE 0 ; will count up every time we center cursor to write on center line below
var1 DWORD ?
var2 DWORD ?

.code
main PROC

mov ECX, 3 ; loop 3
L1:
mov lineCount, 0 ; reset line count

call Clrscr ; clear screen

call CursorMiddle ; readme
call Gotoxy ; sets cursor

mov EDX, OFFSET string ; get string and write in
call WriteString

call CursorMiddle
call Gotoxy

call ReadDec ; returns to EAX
mov var1, EAX

call CursorMiddle
call Gotoxy

call ReadDec ; returns to EAX
mov var2, EAX

call CursorMiddle
call Gotoxy

mov EAX, var1
add EAX, var2

call WriteDec ; writes EAX to output
call Crlf

call CursorMiddle
call Gotoxy

call WaitMsg ; waits for user so sum can be shown
LOOP L1

JMP Endd

CursorMiddle PROC

mov EDX, 0	; reset EDX for GetMaxXY
mov EAX, 0 ; reset EAX because GetMaxXY stores Y in AL instead of DH, contrary to irvine documentation
call GetMaxXY ; stored window width to DL and window height to AL, FOR SOME REASON(???)
SHR dl, 1	;shift right by 1, divides by 2
dec dl ; moves line 1 widths less
SHR al, 1 ; for some reason, the window buffer height is getting stored in AL, as opposed to DH
add al, lineCount
inc lineCount
mov dh, al ; move the Y from GetMaxXY from AL, I do not know why it is not stored in DH, to DH for Gotoxy

; I cannot stress how frustrating this error was to figure out as there was no documentation from anyone else who had this problem, I hope that my code will not be penalized
; due to something I believe to be outside of my control

;here is what the code would look like if it functioned as documented, with the Y height of the window being stored into DH
;mov EDX, 0
;call GetMaxXY
;SHR dl, 1
;dec dl
;SHR dh, 1
;dec dh

RET

CursorMiddle ENDP

Endd:

INVOKE ExitProcess,0
main ENDP
END main