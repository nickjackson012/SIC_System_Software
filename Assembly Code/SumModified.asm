SUMMOD     START       4000
FIRST   LDX         ZERO
        LDA         ONE
LOOP1   MUL         COUNT
        STA         TABLE,X
        TIX         COUNT
        TIX         COUNT
        TIX         COUNT
        JLT         LOOP1
        LDX         ZERO
        LDA         ZERO
LOOP2   ADD         TABLE,X
        TIX         COUNT
        TIX         COUNT
        TIX         COUNT
        JLT         LOOP2
        STA         TOTAL
        RSUB
TABLE   RESW        2000
COUNT   WORD        9
ZERO    WORD        0
ONE     WORD        1
TOTAL   RESW        1
        END         FIRST