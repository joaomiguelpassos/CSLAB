main: asm.o
		gcc main.c asm.o -lsqlite3 -ldl -pthread -lmosquitto -lwiringPi -o main

asm.o: asm.s
		gcc -Wall -g -c asm.s -o asm.o

run: main
		./main

clean:
		rm *.o main