.balign 4
.text
	.globl pin1
    .globl pin2

.balign 4
.global comparePIN

comparePIN:
    ldr r1, =pin1
    ldr r0, [r1]

    ldr r2, =pin2
    ldr r1, [r2]

    CMP r0,r1
    BEQ correctPIN
    BNE incorrectPIN

correctPIN:
    MOV r0, #1
    BX lr

incorrectPIN:
    MOV r0,#0
    BX lr