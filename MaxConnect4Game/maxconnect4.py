import sys
from MaxConnect4Game import *
def oneMoveGame(currentGame,max_depth,inter_flag):
    if currentGame.pieceCount == 42:    # Is the board full already?
        print 'BOARD FULL\n\nGame Over!\n'
	if currentGame.player1Score>currentGame.player2Score:
	    print('Player 1 Wins')	
	elif currentGame.player2Score>currentGame.player1Score:
	    print('Player 2 Wins')
	else:
	    print('It\'s a tie!')			
	sys.exit(0)
	
    if inter_flag==1:
	print('Computer Move')
    currentGame.aiPlay(currentGame.currentTurn,max_depth) # Make a move

    print 'Game state after move:'
    currentGame.printGameBoard()
    currentGame.countScore()
    if currentGame.currentTurn == 1:	
    	currentGame.currentTurn = 2
    else:
	currentGame.currentTurn = 1
    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

    if inter_flag==0:
    	currentGame.printGameBoardToFile()
    	currentGame.gameFile.close()
    else:
	file = currentGame.gameFile
	currentGame.gameFile = open('computer.txt','a')
	currentGame.printGameBoardToFile()
	currentGame.gameFile.close()
	currentGame.gameFile = file

def interactiveGame(currentGame,max_depth,player):
    if player=='human-next':
	
	if currentGame.pieceCount == 42:    # Is the board full already?
            print 'BOARD FULL\n\nGame Over!\n'
	    if currentGame.player1Score>currentGame.player2Score:
		print('Player 1 Wins')
	    elif currentGame.player2Score>currentGame.player1Score:
		print('Player 2 Wins')
	    else:
	    	print('It\'s a tie!')		
            sys.exit(0)
	while True:
	    print('Enter a valid column to make a move')
	    moveColumn = int(input())-1
	    if currentGame.checkMoves(moveColumn):
		break
	currentGame.playPiece(currentGame.gameBoard,moveColumn)
    	currentGame.countScore()
	if currentGame.currentTurn == 1:	
    	    currentGame.currentTurn = 2
    	else:	
    	    currentGame.currentTurn = 1	
	currentGame.checkPieceCount()
	print('Human Move')
	print('Player1, Player2',currentGame.player1Score,currentGame.player2Score)
        print('\n\nmove %d: Player %d, column %d\n' % (currentGame.pieceCount, currentGame.currentTurn, moveColumn+1))
	print 'Game state after move:'
        currentGame.printGameBoard()
    	print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
        file = currentGame.gameFile
	currentGame.gameFile = open('human.txt','a')
	currentGame.printGameBoardToFile()
	currentGame.gameFile.close()
	currentGame.gameFile = file
	#currentGame.printGameBoardToFile()
        #currentGame.gameFile.close()
    else:		
	inter_flag = 1
	oneMoveGame(currentGame,max_depth,inter_flag)
    if player == 'human-next':
	player = 'computer-next'
    else:
	player = 'human-next'
    interactiveGame(currentGame,max_depth,player)	

def main(argv):
    # Make sure we have enough command-line arguments
    open('human.txt', 'w').close()
    open('computer.txt','w').close()	
    if len(argv) != 5:
        print 'Four command-line arguments are needed:'
        print('Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % argv[0])
        print('or: %s one-move [input_file] [output_file] [depth]' % argv[0])
        sys.exit(2)

    game_mode, inFile = argv[1:3]
    out_player = argv[3]
    max_depth = int(argv[4])
    if not game_mode == 'interactive' and not game_mode == 'one-move':
        print('%s is an unrecognized game mode' % game_mode)
        sys.exit(2)
    if game_mode == 'interactive' and out_player!= 'computer-next' and out_player!='human-next':
	print('%s is an unrecognized player'% out_player)
	sys.exit(2) 
	
    currentGame = maxConnect4Game() # Create a game
   
    # Try to open the input file
    try:
        currentGame.gameFile = open(inFile, 'r')
    except IOError:
        sys.exit("\nError opening input file.\nCheck file name.\n")

    # Read the initial game state from the file and save in a 2D list
    file_lines = currentGame.gameFile.readlines()
    currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
    currentGame.currentTurn = int(file_lines[-1][0])
    currentGame.player1 = currentGame.currentTurn
    currentGame.gameFile.close()
    print '\nMaxConnect-4 game\n'
    print('Player 1 symbol is %d'%currentGame.player1)
    if currentGame.player1 ==1:
	p2 = 2
    else:
	p2 = 1	
    print('Player 2 symbol is %d'%p2)		
    print 'Game state before move:'
    currentGame.printGameBoard()

    # Update a few game variables based on initial state and print the score
    currentGame.checkPieceCount()
    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
    if game_mode == 'interactive':
        player = out_player
	if player=='human-next':
	    if currentGame.player1 == 1:	
	    	currentGame.maxSymbol = 2 
	    else:
		currentGame.maxSymbol = 1
    	else:
	    currentGame.maxSymbol = currentGame.player1
	interactiveGame(currentGame,max_depth,player) # Be sure to pass whatever else you need from the command line
    else: 
        # Set up the output file
        outFile = out_player
        currentGame.maxSymbol = currentGame.currentTurn
	try:
            currentGame.gameFile = open(outFile, 'w')
        except:
            sys.exit('Error opening output file.')
	oneMoveGame(currentGame,max_depth,0) # Be sure to pass any other arguments from the command line you might need.


if __name__ == '__main__':
    main(sys.argv)
