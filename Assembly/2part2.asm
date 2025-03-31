; A = (A + B) – (C + D).
.386
.model flat,stdcall
.stack 4096
ExitProcess PROTO, dwExitCode:DWORD

.data
var1 BYTE 255
var2 SBYTE -128
var3 WORD 65535
var4 SWORD -32768
var5 DWORD 4294967295
var6 SDWORD −2147483648
var7 FWORD 0FFFFFFFFFFFFh ; largest is 2^48 -1
var8 QWORD 0FFFFFFFFFFFFFFFFh ; largest is 2^64 -1
var9 TBYTE 0FFFFFFFFFFFFFFFFFFFFh ; largest is 2^80 -1
var10 REAL4 4294967295
var11 REAL8 9999999999
var12 REAL10 9999999999

.code
main PROC


INVOKE ExitProcess,0
main ENDP
END main