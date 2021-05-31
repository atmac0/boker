CC = g++
CFLAGS = -g -Wall -std=c++0x -Iinclude 

all: UT_deck.o UT_limit_holdem.o deck.o limit_holdem.o
	$(CC) $(CFLAGS) -o UT_runner UT_runner.cpp UT_deck.o UT_limit_holdem.o deck.o  limit_holdem.o

UT_deck.o: deck.o
	$(CC) $(CFLAGS) -c UT_deck.cpp

UT_limit_holdem.o: limit_holdem.o
	$(CC) $(CFLAGS) -c UT_limit_holdem.cpp

deck.o:
	$(CC) $(CFLAGS) -c ../deck.cpp

limit_holdem.o:
	$(CC) $(CFLAGS) -c ../limit_holdem.cpp

clean:
	rm UT_runner *.o

