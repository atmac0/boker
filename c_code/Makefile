CC = g++
CFLAGS = -g -Wall -std=c++0x

limit_AI: limit_AI.o deck.o limit_holdem.o
	$(CC) $(CFLAGS) -o limit_AI limit_AI.o deck.o limit_holdem.o

limit_AI.o: limit_AI.cpp deck.h limit_holdem.h
	$(CC) $(CFLAGS) -c limit_AI.cpp

deck.o: deck.cpp deck.h

limit_holdem.o: limit_holdem.cpp limit_holdem.h

clean:
	rm limit_AI limit_AI.o deck.o limit_holdem.o

