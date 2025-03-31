; A = (A + B) – (C + D).
.386
.model flat,stdcall
.stack 4096
ExitProcess PROTO, dwExitCode:DWORD

.data
_under WORD 'under'
$dollar WORD 'dollar'
@at WORD 'atmark'
#pound WORD 'pound'
letter WORD 'letter'

.code
main PROC


INVOKE ExitProcess,0
main ENDP
END main