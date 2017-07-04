import sys
import random
import signal
import time
import copy

INF = float("inf")

class Player42:
  	# The team's entire code to be written under this class
  	def __init__(self):
		pass

  	def evaluate(self,board):
		return 1
  	def evaluate1(self,board):

		heu = 0

		blockmap = (  0 , 1 , 10 , 100 , 1000 )
		boardmap = ( 0 , 1000 , 10000 , 100000, 1000000 )

		blockh = [[ 0 for i in range(4)] for j in range(4)]


		for i in range(4):
			for j in range(4):


				#along rows
				for u in range(4*i, 4*i+4):
					ocount = 0
				  	xcount = 0
				  	for v in range(4*j, 4*j+4):
				  		if board.board_status[u][v] == 'o':
				  			ocount+= 1
				  		elif board.board_status[u][v] == 'x':
				  			xcount+= 1
				  	if xcount > 0 and ocount == 0:
						blockh[i][j] += blockmap[xcount]
					elif xcount == 0 and ocount > 0 :
						blockh[i][j] -= blockmap[ocount]


				#along colomns
				for u in range(4*j, 4*j + 4):
				  	ocount = 0
				  	xcount = 0
				  	for v in range(4*i , 4*i + 4):
				  		if board.board_status[v][u] == 'o':
				  			ocount+= 1
				  		elif board.board_status[v][u] == 'x':
							xcount+= 1
				  	if xcount > 0 and ocount == 0:
						blockh[i][j] += blockmap[xcount]
					elif xcount == 0 and ocount > 0 :
						blockh[i][j] -= blockmap[ocount]


				#along diagnal
				xcount = 0
				ocount = 0
				for u in range(4):
				  	if board.board_status[4*i + u][4*j + u] == 'o':
				  		ocount+= 1
				  	elif board.board_status[4*i + u][4*j + u] == 'x':
				  		xcount+= 1

			  	if xcount > 0 and ocount == 0:
					blockh[i][j] += blockmap[xcount]
				elif xcount == 0 and ocount > 0 :
					blockh[i][j] -= blockmap[ocount]


				#along another diagnal
				xcount = 0
				ocount = 0
				for u in range(4):
				  	if board.board_status[ 4*i + u][4*j + 3 - u] == 'o':
				  		ocount+= 1
					elif board.board_status[4*i + u][4*j + 3 -u] == 'x':
				  		xcount+= 1

			  	if xcount > 0 and ocount == 0:
					blockh[i][j] += blockmap[xcount]
				elif xcount == 0 and ocount > 0 :
					blockh[i][j] -= blockmap[ocount]




		#find xmax , omax
		#along rows
		for u in range(4):
			ocount = 0
		  	xcount = 0
		  	for v in range(4):
		  		if board.block_status[u][v] == 'o':
		  			ocount+= 1
		  		elif board.block_status[u][v] == 'x':
		  			xcount+= 1
		  	if not(xcount > 0 and ocount  > 0):
				if xcount == 0 and ocount > 0 :
					heu -= boardmap[ocount]
				elif xcount > 0 and ocount == 0:
					heu += boardmap[xcount]
		  		for v in range(4):
					if board.block_status[u][v] == '-':
						heu += blockh[u][v]


		#along colomns
		for u in range(4):
		  	ocount = 0
		  	xcount = 0
		  	for v in range(4):
		  		if board.block_status[v][u] == 'o':
		  			ocount+= 1
		  		elif board.block_status[v][u] == 'x':
		  			xcount+= 1
		  	if not(xcount > 0 and ocount  > 0):

				if xcount == 0 and ocount > 0 :
					heu -= boardmap[ocount]
				elif xcount > 0 and ocount == 0:
					heu += boardmap[xcount]
		  		for v in range(4):
					if board.block_status[v][u] == '-':
						heu += blockh[v][u]

		#along diagnal
		xcount = 0
		ocount = 0
		for u in range(4):
		  	if board.block_status[u][u] == 'o':
		  		ocount+= 1
		  	elif board.block_status[u][u] == 'x':
		  		xcount+= 1

		if not(xcount > 0 and ocount > 0):

			if xcount == 0 and ocount > 0 :
				heu -= boardmap[ocount]
			elif xcount > 0 and ocount == 0:
				heu += boardmap[xcount]
	  		for v in range(4):
				if board.block_status[v][v] == '-':
					heu += blockh[v][v]



		#along another diagnal
		xcount = 0
		ocount = 0
		for u in range(4):
		  	if board.block_status[u][3 - u] == 'o':
		  		ocount+= 1
		  	elif board.block_status[u][3 -u] == 'x':
		  		xcount+= 1

		if not(xcount > 0 and ocount > 0):

			if xcount == 0 and ocount > 0 :
				heu -= boardmap[ocount]
			elif xcount > 0 and ocount == 0:
				heu += boardmap[xcount]
	  		for v in range(4):
				if board.block_status[v][3 -v] == '-':
					heu += blockh[v][3 -v]


		return heu


  	def minimax(self, board, old_move, present_d, depth, flag, alpha, beta):
  		status = board.find_terminal_state()

  		if (present_d == depth) or (status[1] == 'WON') or (status[1] == 'DRAW'):

  			return self.evaluate1(board)

  		if flag=='x':
  			best = -10000000 # -10^7
			cells = board.find_valid_move_cells(old_move)
			if len(cells) == 0:
				return self.evaluate1(board)

			if len(cells) > 16 and depth - present_d >= 3:
				#print "len cells ",len(cells)
				#print
				present_d += 1
			for cell in cells:
				#print "ok ",cell[0],cell[1]
				#print
				board.board_status[cell[0]][cell[1]] = flag
				best = max(best,self.minimax(board,(cell[0],cell[1]),present_d+1,depth,chr(ord('x')+ord('o')-ord(flag)),alpha,beta))
				board.board_status[cell[0]][cell[1]] = '-'
				alpha = max(alpha, best)
				if (beta <= alpha):
				  	break

			return best
		elif flag=='o':
			best = 10000000 #10^7
			cells = board.find_valid_move_cells(old_move)
			if len(cells) == 0:
				return self.evaluate1(board)
			if len(cells) > 16 and depth - present_d >= 3:
				present_d += 1
			for cell in cells:
				board.board_status[cell[0]][cell[1]] = flag
				best = min(best,self.minimax(board,(cell[0],cell[1]),present_d+1,depth,chr(ord('x')+ord('o')-ord(flag)),alpha,beta))
				board.board_status[cell[0]][cell[1]] = '-'
				beta = min(beta, best)
				if (beta <= alpha):
					break
			return best

  	def move(self, board, old_move, flag):
		cells = board.find_valid_move_cells(old_move)  	#Found all the possible steps and need to choose one from them

		if (flag=='x'):
		  	bestval = -10000000 # -10^7
		elif (flag=='o'):
		  	bestval = 10000000  # 10^7
		bestrow = -1
		bestcol = -1
		depth = 4
		if len(cells) > 16:
		  	depth = 3
		for cell in cells:
			board.board_status[cell[0]][cell[1]] = flag
			old_move = (cell[0],cell[1])
			moveval = self.minimax(board, old_move, 1, depth, chr(ord('x')+ord('o')-ord(flag)), -INF, INF)
			board.board_status[cell[0]][cell[1]] = '-'
			if flag=='x':  	# maximizer
				if moveval>bestval:
					bestval = moveval
					bestrow = cell[0]
					bestcol = cell[1]
			elif flag=='o': # minimizer
				if moveval<bestval:
					bestval = moveval
					bestrow = cell[0]
					bestcol = cell[1]
		return (bestrow,bestcol)
