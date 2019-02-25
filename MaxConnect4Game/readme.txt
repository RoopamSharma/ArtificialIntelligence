
Instructions for running code:
input file shall be present for running the code
1. one-move mode
   python maxconnect4.py one-move [input-file] [output-file] [max-depth] 
	
2. interactive mode
   python maxconnect4.py interactive [input-file] [human-next/computer-next] [max-depth]

   It generates human.txt and computer.txt storing all the moves made by human and computer respectively.

When input file has 1 as next move 
    if interactive mode has human as next player:
	Player1 is human with symbol 1 
	Player2 is computer with symbol 2
    otherwise if interactive mode has computer as next player:
	Player1 is computer with symbol 1
	Player2 is human with symbol 2

When input file has 2 as next move
    If interactive mode has human as next player:
	Player1 is human with symbol 2
	Player2 is computer with symbol 1
    otherwise if interactive mode has computer as next player:
	Player1 is computer with symbol 2
	Player2 is human with symbol 1

