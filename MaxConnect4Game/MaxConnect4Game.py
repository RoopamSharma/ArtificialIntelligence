import copy
import sys

class maxConnect4Game:
    def __init__(self):
        self.gameBoard = [[0 for i in range(7)] for j in range(6)]
        self.currentTurn = 1
        self.player1Score = 0
        self.player2Score = 0
        self.pieceCount = 0
        self.gameFile = None
        self.player1 = 0
	self.maxSymbol = 0
        
    # Count the number of pieces already played
    def checkPieceCount(self):
        self.pieceCount = sum(1 for row in self.gameBoard for piece in row if piece)

    # Output current game status to console
    def printGameBoard(self):
        print ' -----------------'
        for i in range(6):
            print ' |',
            for j in range(7):
                print('%d' % self.gameBoard[i][j]),
            print '| '
        print ' -----------------'

    # Output current game status to file
    def printGameBoardToFile(self):
        for row in self.gameBoard:
            self.gameFile.write(''.join(str(col) for col in row) + '\r\n')
        self.gameFile.write('%s\r\n' % str(self.currentTurn))

    # Place the current player's piece in the requested column
    def playPiece(self,gameBoard,column):
	for row in range(5,-1,-1):
	    if gameBoard[row][column]==0:
		gameBoard[row][column]=self.currentTurn
		break
	
    # check if move is playable
    def checkMoves(self,column):
	if column not in range(7):
	    return False
        for row in range(5,-1,-1):
	    if self.gameBoard[row][column]==0:
		return True
	return False		
 	
    # The AI section. 
    def aiPlay(self,turn,max_depth):
	# Calling alpha beta pruning method
	moveColumn  = self.alphaBetaDecision(float('-inf'),float('inf'),turn,max_depth)
	self.playPiece(self.gameBoard,moveColumn)
	self.countScore()
	self.checkPieceCount()
	print('Player1, Player2',self.player1Score,self.player2Score)
        print('\n\nMove %d: Player %d, column %d\n' % (self.pieceCount, self.currentTurn, moveColumn+1))
        #if self.currentTurn == 1:
        #    self.currentTurn = 2
        #elif self.currentTurn == 2:
        #    self.currentTurn = 1

    # Alpha beta pruning method
    def alphaBetaDecision(self,alpha,beta,turn,max_depth):
        v,move = self.maxValue(alpha,beta,max_depth,0,turn)
	return move	

    #maxNode method
    def maxValue(self,alpha,beta,depth,ind,turn):
	self.checkPieceCount()
	#print('Calling Parent Max')
	#self.printGameBoard()
	v = -1*sys.maxint-1
	max_i = 0
	if self.pieceCount==42 or depth==0:
	    #self.countScore()
	    #return self.player1Score,ind 
	    #self.printGameBoard()
	    val = self.evalfunc()
	    #print('Max: Score',val)
	    return val,ind	
	else:
	    for i in range(0,7):
		if self.checkMoves(i):
		    sgb = copy.deepcopy(self)
		    sgb.currentTurn = turn
		    sgb.playPiece(sgb.gameBoard,i)
		    #print('Created %dth Child in max'%i)
		    #sgb.printGameBoard()
		    tmp_v,t = sgb.minValue(alpha,beta,depth-1,i,turn)
		    if v<tmp_v:
			v = tmp_v
			max_i = i
		    if v>=beta:
			return v,max_i
		    alpha = max(v,alpha)			
	    return v,max_i

    #minNode method
    def minValue(self,alpha,beta,depth,ind,turn):
	self.checkPieceCount()
 	#print('Calling parent Min')
	#self.printGameBoard()	
	v = sys.maxint
	min_i = 0
	if self.pieceCount==42 or depth==0:
	    #self.countScore()
	    #return self.player1Score,ind	
	    #self.printGameBoard()
	    val = self.evalfunc()
	    #print('Min: Score',val)
	    return val,ind	
	else:
	    for i in range(0,7):
		if self.checkMoves(i):
		    sgb = copy.deepcopy(self)
		    if turn==1:
		    	sgb.currentTurn = 2
		    else: 
			sgb.currentTurn = 1
		    sgb.playPiece(sgb.gameBoard,i)
		    #print('Created %dth child in min'%i)
		    #sgb.printGameBoard()
		    tmp_v,t = sgb.maxValue(alpha,beta,depth-1,i,turn)
		    if v>tmp_v:
			v = tmp_v
			min_i = i 		
		    if v<=alpha:
			return v,min_i
		    beta = min(v,beta)
	    return v,min_i
	
    # Calculate the number of 4-in-a-row each player has
    def countScore(self):
        self.player1Score = 0;
        self.player2Score = 0;
        if self.player1 == 1:
	    p1 = 1
            p2 = 2
	else:
	    p1 = 2
 	    p2 = 1	
        
	# Check horizontally
        for row in self.gameBoard:
            for i in range(0,4):
	    	# Player 1
		if row[i:i+4] == [p1]*4:
                   self.player1Score += 1
           	# Player 2
		elif row[i:i+4] == [p2]*4:
                   self.player2Score += 1

        # Check vertically
        for j in range(7):
	    for i in range(0,3):
		# Player 1
	    	if self.gameBoard[i][j] == p1 and self.gameBoard[i+1][j] == p1 and self.gameBoard[i+2][j] == p1 and self.gameBoard[i+3][j] == p1:
                    self.player1Score += 1
            	# Player 2
		elif self.gameBoard[i][j] == p2 and self.gameBoard[i+1][j] == p2 and self.gameBoard[i+2][j] == p2 and self.gameBoard[i+3][j] == p2:
                    self.player2Score += 1

        # Check diagonally left side
 	for i in range(3,6):       
	    for j in range(0,4):
		# Player 1
		if self.gameBoard[i][j] == p1 and self.gameBoard[i-1][j+1] == p1 and self.gameBoard[i-2][j+2] == p1 and self.gameBoard[i-3][j+3] == p1:
	            self.player1Score += 1
		# Player 2
		elif self.gameBoard[i][j] == p2 and self.gameBoard[i-1][j+1] == p2 and self.gameBoard[i-2][j+2] == p2 and self.gameBoard[i-3][j+3] == p2:
		    self.player2Score += 1

	# Check diagonally right side
	for i in range(2,-1,-1):       
	    for j in range(0,4):
		# Player 1
		if self.gameBoard[i][j] == p1 and self.gameBoard[i+1][j+1] == p1 and self.gameBoard[i+2][j+2] == p1 and self.gameBoard[i+3][j+3] == p1:
	            self.player1Score += 1
		# Player 2
		elif self.gameBoard[i][j] == p2 and self.gameBoard[i+1][j+1] == p2 and self.gameBoard[i+2][j+2] == p2 and self.gameBoard[i+3][j+3] == p2:
		    self.player2Score += 1 

    def evalfunc(self):
	p = self.maxSymbol
	if p == 1:
	    q = 2
	else:
	    q = 1
	score = 0
	
	# 4 in a row for max player is 100 points and 4 in a row for min player is -100 points.
	# 3 in a row for max player is 50 points and 3 in a row for min player is -50 points.
	# 2 in a row for mas player is 25 points and 3 in a row for min player is -25 points.
	# Check horizontally
        for row in self.gameBoard:
            for i in range(0,4):
		if row[i:i+4] == [p]*4:
                    score += 100
		if row[i:i+4] == [q]*4:
		    score -= 100
		if (row[i:i+3] == [p]*3 and row[i+3] == 0) or (row[i+1:i+4] == [p]*3 and row[i] == 0):
		    score += 50
		if (row[i:i+3] == [q]*3 and row[i+3] == 0) or (row[i+1:i+4] == [q]*3 and row[i] == 0):
		    score -= 50
		if (row[i:i+2] == [p]*2 and row[i+2:i+4] == [0,0]) or (row[i:i+2] == [0]*2 and row[i+2:i+4] == [p]*2) or (row[i+1:i+3] == [p]*2 and row[i+3] == 0 and row[i] == 0) or (row[i+1:i+3] == [0]*2 and row[i+3] == p and row[i] == p):
		    score += 30
   		if (row[i:i+2] == [q]*2 and row[i+2:i+4] == [0,0]) or (row[i:i+2] == [0]*2 and row[i+2:i+4] == [q]*2) or (row[i+1:i+3] == [q]*2 and row[i+3] == 0 and row[i] == 0) or (row[i+1:i+3] == [0]*2 and row[i+3] == q and row[i] == q):
		    score -= 30
        #print('HS',score)
	# Check vertically
        for j in range(7):
	    for i in range(0,3):
	    	if self.gameBoard[i][j] == p and self.gameBoard[i+1][j] == p and self.gameBoard[i+2][j] == p and self.gameBoard[i+3][j] == p:
                    score += 100
		if self.gameBoard[i][j] == q and self.gameBoard[i+1][j] == q and self.gameBoard[i+2][j] == q and self.gameBoard[i+3][j] == q:
                    score -= 100
		if self.gameBoard[i][j] == p and self.gameBoard[i+1][j] == p and self.gameBoard[i+2][j] == p and self.gameBoard[i+3][j] == 0:
                    score += 50
		if self.gameBoard[i][j] == q and self.gameBoard[i+1][j] == q and self.gameBoard[i+2][j] == q and self.gameBoard[i+3][j] == 0:
                    score -= 50
		if self.gameBoard[i][j] == p and self.gameBoard[i+1][j] == p and self.gameBoard[i+2][j] == 0 and self.gameBoard[i+3][j] == 0:
                    score += 30
		if self.gameBoard[i][j] == q and self.gameBoard[i+1][j] == q and self.gameBoard[i+2][j] == 0 and self.gameBoard[i+3][j] == 0:
                    score -= 30
	#print('VS',score)
        # Check diagonally left side
 	for i in range(3,6):       
	    for j in range(0,4):
	        if self.gameBoard[i][j] == p and self.gameBoard[i-1][j+1] == p and self.gameBoard[i-2][j+2] == p and self.gameBoard[i-3][j+3] == p:
	            score += 100
            	if self.gameBoard[i][j] == q and self.gameBoard[i-1][j+1] == q and self.gameBoard[i-2][j+2] == q and self.gameBoard[i-3][j+3] == q:
	            score -= 100
            	if ((self.gameBoard[i][j] == p and self.gameBoard[i-1][j+1] == p and self.gameBoard[i-2][j+2] == p and self.gameBoard[i-3][j+3] == 0) or (self.gameBoard[i][j] == 0 and self.gameBoard[i-1][j+1] == p and self.gameBoard[i-2][j+2] == p and self.gameBoard[i-3][j+3] == p)):
	            score += 50
		if ((self.gameBoard[i][j] == q and self.gameBoard[i-1][j+1] == q and self.gameBoard[i-2][j+2] == q and self.gameBoard[i-3][j+3] == 0) or (self.gameBoard[i][j] == 0 and self.gameBoard[i-1][j+1] == q and self.gameBoard[i-2][j+2] == q and self.gameBoard[i-3][j+3] == q)):
		    score -= 50
		if ((self.gameBoard[i][j] == p and self.gameBoard[i-1][j+1] == p and self.gameBoard[i-2][j+2] == 0 and self.gameBoard[i-3][j+3] == 0) or (self.gameBoard[i][j] == 0 and self.gameBoard[i-1][j+1] == 0 and self.gameBoard[i-2][j+2] == p and self.gameBoard[i-3][j+3] == p) or (self.gameBoard[i][j] == 0 and self.gameBoard[i-1][j+1] == p and self.gameBoard[i-2][j+2] == p and self.gameBoard[i-3][j+3] == 0) or (self.gameBoard[i][j] == p and self.gameBoard[i-1][j+1] == 0 and self.gameBoard[i-2][j+2] == 0 and self.gameBoard[i-3][j+3] == p)):
		    score += 30
	   	if ((self.gameBoard[i][j] == q and self.gameBoard[i-1][j+1] == q and self.gameBoard[i-2][j+2] == 0 and self.gameBoard[i-3][j+3] == 0) or (self.gameBoard[i][j] == 0 and self.gameBoard[i-1][j+1] == 0 and self.gameBoard[i-2][j+2] == q and self.gameBoard[i-3][j+3] == q) or (self.gameBoard[i][j] == 0 and self.gameBoard[i-1][j+1] == q and self.gameBoard[i-2][j+2] == q and self.gameBoard[i-3][j+3] == 0) or (self.gameBoard[i][j] == q and self.gameBoard[i-1][j+1] == 0 and self.gameBoard[i-2][j+2] == 0 and self.gameBoard[i-3][j+3] == q)):
		    score -= 30 
       # print('LD',score)     	    	
	# Check diagonally right side
	for i in range(2,-1,-1):       
	    for j in range(0,4):
		if self.gameBoard[i][j] == p and self.gameBoard[i+1][j+1] == p and self.gameBoard[i+2][j+2] == p and self.gameBoard[i+3][j+3] == p:
	    	    score += 100
		if self.gameBoard[i][j] == q and self.gameBoard[i+1][j+1] == q and self.gameBoard[i+2][j+2] == q and self.gameBoard[i+3][j+3] == q:
	    	    score -= 100
		if ((self.gameBoard[i][j] == p and self.gameBoard[i+1][j+1] == p and self.gameBoard[i+2][j+2] == p and self.gameBoard[i+3][j+3] == 0) or (self.gameBoard[i][j] == 0 and self.gameBoard[i+1][j+1] == p and self.gameBoard[i+2][j+2] == p and self.gameBoard[i+3][j+3] == p)):
	            score += 50
		if ((self.gameBoard[i][j] == q and self.gameBoard[i+1][j+1] == q and self.gameBoard[i+2][j+2] == q and self.gameBoard[i+3][j+3] == 0) or (self.gameBoard[i][j] == 0 and self.gameBoard[i+1][j+1] == q and self.gameBoard[i+2][j+2] == q and self.gameBoard[i+3][j+3] == q)):
		    score -= 50
		if ((self.gameBoard[i][j] == p and self.gameBoard[i+1][j+1] == p and self.gameBoard[i+2][j+2] == 0 and self.gameBoard[i+3][j+3] == 0) or (self.gameBoard[i][j] == 0 and self.gameBoard[i+1][j+1] == 0 and self.gameBoard[i+2][j+2] == p and self.gameBoard[i+3][j+3] == p) or (self.gameBoard[i][j] == 0 and self.gameBoard[i+1][j+1] == p and self.gameBoard[i+2][j+2] == p and self.gameBoard[i+3][j+3] == 0) or (self.gameBoard[i][j] == p and self.gameBoard[i+1][j+1] == 0 and self.gameBoard[i+2][j+2] == 0 and self.gameBoard[i+3][j+3] == p)):
		    score += 30
	   	if ((self.gameBoard[i][j] == q and self.gameBoard[i+1][j+1] == q and self.gameBoard[i+2][j+2] == 0 and self.gameBoard[i+3][j+3] == 0) or (self.gameBoard[i][j] == 0 and self.gameBoard[i+1][j+1] == 0 and self.gameBoard[i+2][j+2] == q and self.gameBoard[i+3][j+3] == q) or (self.gameBoard[i][j] == 0 and self.gameBoard[i+1][j+1] == q and self.gameBoard[i+2][j+2] == q and self.gameBoard[i+3][j+3] == 0) or (self.gameBoard[i][j] == q and self.gameBoard[i+1][j+1] == 0 and self.gameBoard[i+2][j+2] == 0 and self.gameBoard[i+3][j+3] == q)):
		    score -= 30 
	#print('RD',score)
        return score 
