main: main.o sqlite3.o asm.o
		gcc main.o asm.o sqlite3.o -o main

main.o: main.c sqlite3.o
		gcc -Wall -g -c main.c -o main.o

sqlite3.o: sqlite3.c
		gcc sqlite3.c -I /sqlite3/ -lpthread -ldl -lm -o sqlite3.o

asm.o: asm.s
		gcc -Wall -g -c asm.s -o asm.o

run: main
		./main

clean:
		rm *.o main