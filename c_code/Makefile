CC = g++
CFLAGS = -g -Wall -std=c++0x

all: limit_AI limit_terminal

limit_AI: limit_AI.o
	$(CC) $(CFLAGS) -o limit_AI limit_AI.o deck.o limit_holdem.o

limit_terminal: limit_terminal.o
	$(CC) $(CFLAGS) -o limit_terminal limit_terminal.o deck.o limit_holdem.o

limit_AI.o: deck.o limit_holdem.o
	$(CC) $(CFLAGS) -c limit_AI.cpp


limit_terminal.o: limit_holdem.o
	$(CC) $(CFLAGS) -c limit_terminal.cpp

deck.o:
	$(CC) $(CFLAGS) -c deck.cpp

limit_holdem.o:
	$(CC) $(CFLAGS) -c limit_holdem.cpp

clean:
	rm limit_AI limit_AI.o deck.o limit_holdem.o

