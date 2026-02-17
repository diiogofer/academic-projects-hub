TIME = 0
COUNTERS = 0
FINAL = 0

DELIVER = 1

PRE_PROCESS = 0
DEBUG = 0
STAGES = 0
FILTER = 0
ACTIONS = 0
RESULT = 0

LETTERS = {'I', 'L', 'S', 'T'}

ALL_DIR = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

ORT_DIR = [(-1,0), (1,0), (0,-1), (0,1)]

SQUARE_OFFSETS = [
	[(0, 0), (1, 0), (0, 1), (1, 1)],   # bottom-right
	[(0, 0), (1, 0), (0, -1), (1, -1)], # bottom-left
	[(0, 0), (-1, 0), (0, 1), (-1, 1)], # top-right
	[(0, 0), (-1, 0), (0, -1), (-1, -1)]# top-left
]

PIECES = [
	{
		'type': 'L',
		'letter': 'L',
		'piece_shape': [(0,0),(1,0),(2,0),(2,1)],
		'special_cells': [(1,1)]
	},
	{
		'type': 'L1',
		'letter': 'L',
		'piece_shape': [(0,0),(0,1),(0,2),(1,0)],
		'special_cells': [(1,1)]
	},
	{
		'type': 'L2',
		'letter': 'L',
		'piece_shape': [(0,0),(0,1),(1,1),(2,1)],
		'special_cells': [(1,0)]
	},
	{
		'type': 'L3',
		'letter': 'L',
		'piece_shape': [(0,0),(0,1),(0,2),(-1,2)],
		'special_cells': [(-1,1)]
	},
	{
		'type': 'L4',
		'letter': 'L',
		'piece_shape': [(0,0),(1,0),(2,0),(2,-1)],
		'special_cells': [(1,-1)]
	},
	{
		'type': 'L5',
		'letter': 'L',
		'piece_shape': [(0,0),(1,0),(1,1),(1,2)],
		'special_cells': [(0,1)]
	},
	{
		'type': 'L6',
		'letter': 'L',
		'piece_shape': [(0,0),(0,1),(1,0),(2,0)],
		'special_cells': [(1,1)]
	},
	{
		'type': 'L7',
		'letter': 'L',
		'piece_shape': [(0,0),(0,1),(0,2),(1,2)],
		'special_cells': [(1,1)]
	},
	{
		'type': 'I',
		'letter': 'I',
		'piece_shape': [(0,0),(1,0),(2,0),(3,0)],
		'special_cells': []
	},
	{
		'type': 'I1',
		'letter': 'I',
		'piece_shape': [(0,0),(0,1),(0,2),(0,3)],
		'special_cells': []
	},
	{
		'type': 'T',
		'letter': 'T',
		'piece_shape': [(0,0),(0,1),(0,2),(1,1)],
		'special_cells': [(1,0),(1,2)]
	},
	{
		'type': 'T1',
		'letter': 'T',
		'piece_shape': [(0,0),(0,1),(-1,1),(1,1)],
		'special_cells': [(-1,0),(1,0)]
	},
	{
		'type': 'T2',
		'letter': 'T',
		'piece_shape': [(0,0),(1,0),(1,1),(1,-1)],
		'special_cells': [(0,-1),(0,1)]
	},
	{
		'type': 'T3',
		'letter': 'T',
		'piece_shape': [(0,0),(1,0),(1,1),(2,0)],
		'special_cells': [(0,1),(2,1)]
	},
	{
		'type': 'S',
		'letter': 'S',
		'piece_shape': [(0,0),(1,0),(1,1),(2,1)],
		'special_cells': [(2,0),(0,1)]
	},
	{
		'type': 'S1',
		'letter': 'S',
		'piece_shape': [(0,0),(0,1),(-1,1),(-1,2)],
		'special_cells': [(0,2),(-1,0)]
	},
	{
		'type': 'S2',
		'letter': 'S',
		'piece_shape': [(0,0),(-1,0),(-1,1),(-2,1)],
		'special_cells': [(-2,0),(0,1)]
	},
	{
		'type': 'S3',
		'letter': 'S',
		'piece_shape': [(0,0),(0,1),(1,1),(1,2)],
		'special_cells': [(1,0),(0,2)]
	}
]

