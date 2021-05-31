CC = g++
CFLAGS = -g -Wall -std=c++0x

all: limit_AI.o deck.o limit_holdem.o types.o
	$(CC) $(CFLAGS) -o limit_AI limit_AI.o deck.o limit_holdem.o types.o

limit_AI.o: limit_AI.cpp deck.h limit_holdem.h
	$(CC) $(CFLAGS) -c limit_AI.cpp

deck.o: deck.cpp deck.h

limit_holdem.o: limit_holdem.cpp limit_holdem.h

types.o: types.h

clean:
	rm limit_AI limit_AI.o deck.o limit_holdem.o types.o

