# ppcasm2plan9
Script to translate power assembly to go lang plan9 assembly

```programming
$ cat example.S 
.Loop:
        add 16,16,20
        add 17,17,21
        xor 28,28,16
        xor 29,29,17
        rotlwi 28,28,16
        rotlwi 29,29,16
        add 24,24,28
        add 25,25,29
        xor 20,20,24
        xor 21,21,25
        rotlwi 20,20,12
        rotlwi 21,21,12

$ ./ppcasm2plan9.py example.S 
loop:
        ADD R20, R16, R16              // add 16,16,20
        ADD R21, R17, R17              // add 17,17,21
        XOR R16, R28, R28              // xor 28,28,16
        XOR R17, R29, R29              // xor 29,29,17
        ROTLW $16, R28, R28            // rotlwi 28,28,16
        ROTLW $16, R29, R29            // rotlwi 29,29,16
        ADD R28, R24, R24              // add 24,24,28
        ADD R29, R25, R25              // add 25,25,29
        XOR R24, R20, R20              // xor 20,20,24
        XOR R25, R21, R21              // xor 21,21,25
        ROTLW $12, R20, R20            // rotlwi 20,20,12
        ROTLW $12, R21, R21            // rotlwi 21,21,12
```
