CC = gcc
CFLAGS = -c -g -Wall -Wextra
LFLAGS = -Wall -Wextra -pthread

.PHONY: all clean

all: threadMatrixMult threadMonte threadAddition

threadAddition: obj/threadAddition.o
	$(CC) $(LFLAGS) $^ -o $@

threadMatrixMult: obj/threadMatrixMult.o
	$(CC) $(LFLAGS) $^ -o $@

threadMonte: obj/threadMonte.o
	$(CC) $(LFLAGS) $^ -o $@

obj/threadAddition.o: src/threadAddition.c
	$(CC) $(CFLAGS) $< -o $@

obj/threadMatrixMult.o: src/threadMatrixMult.c
	$(CC) $(CFLAGS) $< -o $@

obj/threadMonte.o: src/threadMonte.c
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -f threadAddition
	rm -f threadMatrixMult
	rm -f threadMonte
	rm -f threadSort
	rm -f time.txt
	rm -f obj/*.o
	rm -f *~
	rm -f results/Addition/results*.txt
	rm -f results/FileProc/results*.txt
	rm -f results/time.txt
