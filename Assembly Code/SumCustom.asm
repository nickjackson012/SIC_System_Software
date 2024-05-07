SUMCUS     START       4000
FIRST   LDX         ZERO
        LDA         ONE
LOOP1   MUL         COUNT
        STA         TABLE,X
        TXW         COUNT
        JLT         LOOP1
        LDX         ZERO
        LDA         ZERO
LOOP2   ADD         TABLE,X
        TXW         COUNT
        JLT         LOOP2
        STA         TOTAL
        XOS
TABLE   RESW        2000
COUNT   WORD        3
ZERO    WORD        0
ONE     WORD        1
TOTAL   RESW        1
        END         FIRST