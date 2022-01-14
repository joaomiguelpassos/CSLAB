.balign 4
.text
	.global pin1
    .global pin2

.balign 4
.global comparePIN

comparePIN:
    MOV R0, =pin1
    MOV R1, =pin2
    CMP R0, R1
    BEQ correctPIN
    MOV R0, #0
    BX lr

correctPIN:
    MOV R0, #1
    BX lr