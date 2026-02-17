# Grupo 21:
# 110306 Diogo Fernandes
# 63484 Michael Maycock


from search import *
from constants import *
from sys import stdin
from collections import deque

if(TIME): import time

BOARD_START = None
BOARD_SIZE = None
REGIONS_AMOUNT = None
REGIONS = None
REGIONS_NEIGHBORS = None
REGIONS_BORDER = None
REGIONS_ACTIONS = None

STATES_COUNTER = 0


class NuruominoState:
	state_id = 0

	def __init__(self, board, regions_actions, regions_action, valid, regions_filled = None, regions_changed = None):
		self.id = NuruominoState.state_id
		NuruominoState.state_id += 1

		self.board = board

		self.regions_actions_old = regions_actions
		self.regions_actions_new = {}

		self.regions_action = regions_action

		self.valid = valid

		if regions_filled is None:
			self.regions_filled = [0] * REGIONS_AMOUNT
		else:
			self.regions_filled = regions_filled

		if regions_changed is None:
			self.regions_changed = [0] * REGIONS_AMOUNT
		else:
			self.regions_changed = regions_changed

		if DEBUG: 
			print('BOARD')
			pretty_print(board)
		
		if COUNTERS: 
			global STATES_COUNTER
			STATES_COUNTER += 1

	def check_dead_end(self, action):
		_, _, path, _ = action
		board = self.board
		regions_filled = self.regions_filled
		# print(path)
		# pretty_print(board)

		visited = set(path)
		queue = deque(path)
		visited_regions = set()
		all_regions = set()

		while queue:
				r, c = queue.popleft()
				current_region = BOARD_START[r][c]
				# current_region_index = int(current_region) - 1
				visited_regions.add(current_region)
				all_regions.add(current_region)

				for nr, nc in board.ortogonal_positions(r, c):
						if (nr, nc) in visited:
								continue
						cell_value = board[nr][nc]

						if cell_value in LETTERS:
								visited.add((nr, nc))
								queue.append((nr, nc))
						else:
								neighbor_region = BOARD_START[nr][nc]
								neighbor_region_index = int(neighbor_region) - 1
								if not regions_filled[neighbor_region_index]:
									all_regions.add(neighbor_region)

		# print(all_regions)
		# print(visited_regions)
		# print(visited)
		if len(all_regions) == REGIONS_AMOUNT: return False
		return len(all_regions) == len(visited_regions)






	def __lt__(self, other):
		""" Este método é utilizado em caso de empate na gestão da lista
		de abertos nas procuras informadas. """
		return self.id < other.id

class Board(list):
	"""Representação interna de um tabuleiro do Puzzle Nuruomino."""

	def __init__(self, board):
		super().__init__(board)

	# def adjacent_regions(self, region:int) -> list:
	# 	"""Devolve uma lista das regiões que fazem fronteira com a região enviada no argumento."""
	# 	#TODO
	# 	pass
	
	def adjacent_positions(self, row:int, col:int) -> list:
		"""Devolve as posições adjacentes à região, em todas as direções, incluindo diagonais."""
		positions = []

		for dr, dc in ALL_DIR:
			r, c = row + dr, col + dc
			if 0 <= r < len(self) and 0 <= c < len(self[0]):
				positions.append((r, c))

		return positions


	def adjacent_values(self, row:int, col:int) -> list:
		"""Devolve os valores das celulas adjacentes à região, em todas as direções, incluindo diagonais."""
		values = []
		for r, c in self.adjacent_positions(row, col):
			values.append(self[r][c])
		return values

	def ortogonal_positions(self, row:int, col:int) -> list:
		positions = []

		for dr, dc in ORT_DIR:
			r, c = row + dr, col + dc
			if 0 <= r < len(self) and 0 <= c < len(self[0]):
				positions.append((r, c))

		return positions
	
	def ortogonal_values(self, row:int, col:int) -> list:
		"""Devolve os valores das celulas adjacentes à região, em todas as direções"""
		values = []
		for r, c in self.ortogonal_positions(row, col):
			if BOARD_START[r][c] == BOARD_START[row][col]: continue
			else: values.append(self[r][c])
		return values
	
	def __str__(self) -> str:
		return '\n'.join(
				'\t'.join(
						str(BOARD_START[row_idx][col_idx]) if cell == 'X' else str(cell)
						for col_idx, cell in enumerate(row)
				)
				for row_idx, row in enumerate(self)
		)
	
	@staticmethod
	def parse_instance():
		"""Lê o test do standard input (stdin) que é passado como argumento
		e retorna uma instância da classe Board.

		Por exemplo:
			$ python3 pipe.py < test-01.txt

			> from sys import stdin
			> line = stdin.readline().split()
		"""
		lines = [line.split() for line in stdin]
		board = Board(lines)
		return board

	# TODO: outros metodos da classe Board

class Nuruomino(Problem):
	def __init__(self, board: Board):
		"""O construtor especifica o estado inicial."""
		empty_actions = [() for _ in range(REGIONS_AMOUNT)]
		NURUOMINO_START = NuruominoState(board, REGIONS_ACTIONS, empty_actions, True)
		super().__init__(NURUOMINO_START)

	def actions(self, state: NuruominoState):
		"""Retorna uma lista de ações que podem ser executadas a
		partir do estado passado como argumento."""
		
		# last action wasn't valid
		if not state.valid: return []

		# new actions per region dictionary
		state.regions_actions_new = {}

		# check every region for edge cases
		for region_index in range(REGIONS_AMOUNT):
			# region without piece and no possible actions
			if not state.regions_filled[region_index] and region_index + 1 not in state.regions_actions_old:
				return []
			# region that borders last action and is now dead end
			if state.regions_filled[region_index] and state.regions_changed[region_index]:
				if state.check_dead_end(state.regions_action[region_index]): return []


		# filter actions per region
		for region in state.regions_actions_old:
			region_index = region -1
			
			# region filled, don't need actions
			if state.regions_filled[region_index]: continue

			# region wasn't changed in last action, no need to filter
			if not state.regions_changed[region_index]:
				state.regions_actions_new[region] = state.regions_actions_old[region]
				continue
			
			# region was changed so must be filtered	
			# wich actions are valid?
			for action in state.regions_actions_old[region]:
				# action is valid ?
				valid = is_action_valid(action, state)

				if valid:
					if region not in state.regions_actions_new:
						state.regions_actions_new[region] = []
					state.regions_actions_new[region].append(action)

		if not state.regions_actions_new: return []

		shortest_region = min(state.regions_actions_new, key=lambda k: len(state.regions_actions_new[k]))
		return state.regions_actions_new[shortest_region]	

	def result(self, state: NuruominoState, action):
		"""Retorna o estado resultante de executar a 'action' sobre
		'state' passado como argumento. A ação a executar deve ser uma
		das presentes na lista obtida pela execução de
		self.actions(state)."""
		if STAGES: print('RESULT')
		region, piece, path, x = action
		region_index = region - 1
		
		dead_end = state.check_dead_end(action)
		if dead_end:
			return NuruominoState(state.board, state.regions_actions_new, state.regions_action, False)

		new_board = Board([line[:] for line in state.board])
		new_regions_action = state.regions_action[:]
		new_regions_filled = state.regions_filled[:]
		regions_changed = [0] * REGIONS_AMOUNT
		
		# regions bordering action's region as a bitmap
		for c_region in REGIONS_NEIGHBORS[region_index]:
			c_index = c_region - 1
			regions_changed[c_index] = 1
		
		new_regions_filled[region_index] = 1

		for (row, col) in x:
			new_board[row][col] = 'X'

		for (row, col) in path:
			new_board[row][col] = piece

		new_regions_action[region_index] = action

		must_touch, must_coords = check_must_touch(region, piece, path, new_board, new_regions_filled)
		if must_touch == 0: return NuruominoState(state.board, state.regions_actions_new, state.regions_action, False)
		if must_touch == 1:
			new_actions = {}
			for region in state.regions_actions_new:
				region_index = region - 1

				if new_regions_filled[region_index]: continue

				if not regions_changed[region_index]:
					new_actions[region] = state.regions_actions_new[region]
					continue

				if region not in must_coords:
					new_actions[region] = state.regions_actions_new[region]
				else:
					must_set = set(must_coords[region])
					for action in state.regions_actions_new[region]:
						_, _, path, _ = action
						if any(coord in must_set for coord in path):
							if region not in new_actions:
								new_actions[region] = []
							new_actions[region].append(action)

			return NuruominoState(new_board, new_actions, new_regions_action, True, new_regions_filled, regions_changed)

		else: return NuruominoState(new_board, state.regions_actions_new, new_regions_action, True, new_regions_filled, regions_changed)

	def goal_test(self, state: NuruominoState):
		"""Retorna True se e só se o estado passado como argumento é
		um estado objetivo. Deve verificar se todas as posições do tabuleiro
		estão preenchidas de acordo com as regras do problema."""
		if STAGES: print('GOAL TEST')
		if not all(state.regions_filled):
			return False

		# if not self.check_equal_adjacents_different_region(state.board):
		#     return False
		if not self.check_connectivity(state.board):
			return False
		return True

	def check_connectivity(self, board: Board):
		""" Todas as peças que estão preenchidas devem formar um único componente ortogonalmente conectado"""
		filled_coords = [(x,y) for x in range(BOARD_SIZE) for y in range(BOARD_SIZE) if board[x][y] in LETTERS]

		visited = set()
		stack = [filled_coords[0]]

		while stack:
			x, y = stack.pop()
			if (x,y) in visited:
				continue
			visited.add((x,y))
			adj = board.ortogonal_positions(x , y) 
			for nx, ny in adj:
				if board[nx][ny] in LETTERS and (nx, ny) not in visited:
					stack.append((nx, ny)) 

		return len(visited) == len(filled_coords)

	def h(self, node: Node):
		"""Função heuristica utilizada para a procura A*."""
		# TODO
		pass

#FUNCOES AUXILIARES NURUOMINO

def is_action_valid(action: tuple, state: NuruominoState):
	region, piece, path, x = action
	board = state.board
	path_set = set(path)
	in_play = False

	for row, col in path:
		# action path has a X
		if board[row][col] == 'X': 
			return False

		for o_row, o_col in board.ortogonal_positions(row, col):
			# out of bounds
			if not (0 <= o_row < BOARD_SIZE and 0 <= o_col < BOARD_SIZE): continue
			o_region = int(BOARD_START[o_row][o_col])
			o_index = o_region - 1
			# ortogonal neighbor region has same piece
			if o_region != region and board[o_row][o_col] == piece:
				return False
			
			# in-play logic 
			if o_region != region and (not state.regions_filled[o_index] or board[o_row][o_col] in LETTERS):
				in_play = True
			
		# 2x2 formation check
		for square in SQUARE_OFFSETS:
			square_coords = [(row + dr, col + dc) for dr, dc in square]
			if any(not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE) for r, c in square_coords): continue
			if all((r, c) in path_set or board[r][c] in LETTERS for r, c in square_coords): return False
		
		# check action X coords don't have a piece in the board
		for row, col in x:
			if board[row][col] in LETTERS: return False

	return in_play



def check_border_coord_is_valid(row: int, col: int, region: int, board: Board, regions_filled: list):
	'''border coord is valid if it has a bordering region wich is either empty or has a piece bordeing it'''
	if board[row][col] == 'X': return False
	ort_coords = board.ortogonal_positions(row, col)
	for o_row, o_col in ort_coords:
		if not (0 <= o_row < BOARD_SIZE and 0 <= o_col < BOARD_SIZE): continue
		o_region = int(BOARD_START[o_row][o_col])
		o_region_index = o_region - 1
		if o_region != region and (not regions_filled[o_region_index] or board[o_row][o_col] in LETTERS):
			return True
	return False		

def get_regions_changed(region: int, path: list):
	regions_changed = [0] * REGIONS_AMOUNT
	for row, col in path:
		for val in BOARD_START.ortogonal_values(row, col):
			adj_region = int(val)
			if adj_region != region: regions_changed[adj_region - 1] = 1
	return regions_changed


def check_must_touch(region: int, piece: str, path: list, board: Board, regions_filled: list):
	coords = {}
	for row, col in path:
		ort_coords = board.ortogonal_positions(row, col)
		for o_row, o_col in ort_coords:
			o_region = int(BOARD_START[o_row][o_col])
			o_region_index = int(o_region) - 1
			if o_region != region:
				#regiao que toca tem uma peça na fronteira
				if board[o_row][o_col] in LETTERS:
					return 2, {}
				#regiao que toca tem peça sem estar na fronteira
				if regions_filled[o_region_index] or board[o_row][o_col] == 'X':
					continue
				#regiao que toca nao tem peça
				else:
					if o_region not in coords:
						coords[o_region] = []
					coords[o_region].append((o_row, o_col))
	if len(coords) > 1: return 2, {}
	if not coords: return 0, {}
	if len(coords) == 1: return 1, coords
			
			

		

def action_X(x_coords: list, board: Board):
	for (row, col) in x_coords:
		if board[row][col] in PIECES: return False
	return True

def action_path(letter: str, path_coords: list, board: Board):
	for (row, col) in path_coords:
		val = board[row][col]
		if val == 'X': 
			if FILTER: print('FILTERED BY X IN PATH')
			return False
		if letter in board.ortogonal_values(row, col): 
			if FILTER: print('FILTERED BY SAME ORTOGONAL')
			return False
		for offsets in SQUARE_OFFSETS:
			count = 0
			for dr, dc in offsets:
				nr, nc = row + dr, col + dc
				if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
					if (nr, nc) in path_coords or board[nr][nc] in LETTERS:
						count += 1
			if count == 4: 
				if FILTER: print('FILTERED BY 2x2')
				return False
	return True

# PRE PROCESSAMENTO
def pre_process():
	global BOARD_START, BOARD_SIZE, REGIONS, REGIONS_AMOUNT, REGIONS_NEIGHBORS, REGIONS_BORDER, REGIONS_ACTIONS
	BOARD_START = Board.parse_instance()
	BOARD_SIZE = len(BOARD_START)
	REGIONS_AMOUNT = count_regions(BOARD_START)
	REGIONS = get_regions(BOARD_START)
	REGIONS_NEIGHBORS, REGIONS_BORDER = get_regions_border(REGIONS, BOARD_START)
	get_starting_actions()

def count_regions(board):
	ids = set()
	for row in range(BOARD_SIZE):
		for col in range(BOARD_SIZE):
			id = board[row][col]
			ids.add(id)
	return len(ids)

def get_regions(board: Board) -> list:
		regions = [[] for _ in range(REGIONS_AMOUNT)]

		for row in range(BOARD_SIZE):
				for col in range(BOARD_SIZE):
						id = board[row][col]
						index = int(id) - 1
						regions[index].append((row,col))

		return regions

def get_regions_border(regions: list, board: Board) -> tuple[list, list]:
	neighbors = [set() for _ in range(REGIONS_AMOUNT)]
	border = [set() for _ in range(REGIONS_AMOUNT)]

	for i in range(REGIONS_AMOUNT):
		region_value = str(i + 1)
		for (row, col) in regions[i]:
			adj_values = board.ortogonal_values(row, col)
			for val in adj_values:
				if str(val) != region_value:
					neighbors[i].add(int(val))
					border[i].add((row, col))

	return neighbors, border

def get_starting_actions():
	global REGIONS_ACTIONS

	regions_actions_dict = {}
	for p in PIECES:
		for i in range(REGIONS_AMOUNT):
			region_value = str(i + 1)
			for (r, c) in REGIONS[i]:
				bordering = False
				valid = True

				path  = []
				x = []

				for (p_r, p_c) in p['piece_shape']:
					nr = r + p_r
					nc = c + p_c

					if not (0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE):
						valid = False
						break

					if BOARD_START[nr][nc] != region_value:
						valid = False
						break

					if (nr, nc) in REGIONS_BORDER[i]:
						bordering = True

					path.append((nr, nc))

				if not bordering or not valid:
					continue

				for(x_r, x_c) in p['special_cells']:
					nr = r + x_r
					nc = c + x_c

					x.append((nr, nc))
				
				else:
					if i + 1 not in regions_actions_dict:
						regions_actions_dict[i + 1] = []
					regions_actions_dict[i + 1].append((i + 1, p['letter'], path, x))

	REGIONS_ACTIONS = regions_actions_dict

def pretty_print(grid1):

	# Define colors per piece type
	color_map = {
		'L': '\033[91m',  # Red
		'S': '\033[92m',  # Green
		'I': '\033[94m',  # Blue
		'T': '\033[93m',  # Yellow
		# add more if needed
	}

	RESET = '\033[0m'
	for r in range(BOARD_SIZE):
		row_out = []
		for c in range(BOARD_SIZE):
				piece = grid1[r][c]
				color = color_map.get(piece, '')  # default no color if unknown piece
				cell_str = f"{color}{piece}{RESET}" if piece != ' ' else ' '
				row_out.append(cell_str)
		print('\t'.join(row_out))

if __name__ == "__main__":
	if TIME: start = time.time()

	pre_process()



	if TIME: chrono = time.time() - start 
	if PRE_PROCESS:
		print('STARTING BOARD:')
		print(BOARD_START)
		print('\nBOARD SIZE:')
		print(BOARD_SIZE)
		print('\nNUMBER OF REGIONS:')
		print(REGIONS_AMOUNT)
		print('REGIONS')
		print(REGIONS)
		print('REGIONS BORDER')
		print(REGIONS_BORDER)
		print('REGIONS NEIGHBORS')
		print(REGIONS_NEIGHBORS)
		print('ACTIONS BY REGION')
		for region in REGIONS_ACTIONS:
			print('REGION', region)
			print(REGIONS_ACTIONS[region])
		print(f'TIME: {chrono:.5f} s')
	
	PROBLEM = Nuruomino(BOARD_START)
	RESULT = depth_first_tree_search(PROBLEM)
	
	if FINAL: pretty_print(RESULT.state.board)
	if COUNTERS:
		print('NUMBER OF STATES:', STATES_COUNTER)
	if TIME:
		chrono = time.time() - start
		print(f'TIME: {chrono:.5f} s')

	if DELIVER: print(RESULT.state.board, end='')
	
	