. Based on ReadWrite.asm (pg. 45)
. Used to test the SIC Assembler and the SIC Simulator
.LABEL	OPCODE	OPERAND		REMARKS
COPY	START	1000			COPY FILE FROM INPUT TO OUTPUT
FIRST	STL		RETADR			SAVE RETURN ADDRESS
CLOOP	JSUB	RDREC			READ INPUT RECORD
		LDA		LENGTH			TEST FOR EOF (LENGTH = 0)
		COMP	ZERO			
		JEQ		ENDFIL			EXIT IF EOF FOUND
		JSUB	WRREC			WRITE OUTPUT RECORD
		J		CLOOP			LOOP
ENDFIL	LDA		EOF				INSERT END OF FILE MARKER
		STA		BUFFER
		LDA		THREE			SET LENGTH = 3
		STA		LENGTH
		JSUB	WRREC			WRITE EOF
		LDL		RETADR			GET RETURN ADDRESS
		RSUB					RETURN TO CALLER	
EOF		BYTE	C'EOF'
THREE	WORD	3
ZERO	WORD	0
RETADR	RESW	1
LENGTH	RESW	1				LENGTH OF RECORD
BUFFER	RESB	4096			4096-BYTE BUFFER AREA
.
.		SUBROUTINE TO READ RECORD INTO BUFFER
.
RDREC	LDX		ZERO			CLEAR LOOP COUNTER
		LDA		ZERO			CLEAR A TO ZERO
RLOOP	TD		INPUT			TEST INPUT DEVICE
		JEQ		RLOOP			LOOP UNTIL READY
		RD		INPUT			READ CHARACTER INTO REGISTER ADDRESS
		COMP	ZERO			TEST FOR END OF RECORD (X'00')
		JEQ		EXIT			EXIT LOOP IF EOR
		STCH	BUFFER,X		STORE CHARACTER IN BUFFER
		TIX		MAXLEN			LOOP UNLESS MAX LENGTH
		JLT		RLOOP			  HAS BEEN REACHED
EXIT	STX		LENGTH			SAVE RECORD LENGTH
		RSUB					RETURN TO CALLER
INPUT	BYTE	X'F1'			CODE FOR INPUT DEVICE
MAXLEN	WORD	4096
.
.		SUBROUTINE TO WRITE RECORD FROM BUFFER
.
WRREC	LDX		ZERO			CLEAR LOOP COUNTER
WLOOP	TD		OUTPUT			TEST OUTPUT DEVICE
		JEQ		WLOOP			LOOP UNTIL READY
		LDCH	BUFFER,X		GET CHARACTER FROM BUFFER
		WD		OUTPUT			WRITE CHARACTER
		TIX		LENGTH			LOOP UNTIL ALL CHARACTERS
		JLT		WLOOP			  HAVE BEEN WRITTEN
		RSUB					RETURN TO CALLER
OUTPUT	BYTE	X'05'			CODE FOR OUTPUT DEVICE
		END		FIRST	