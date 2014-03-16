import random

def memoize(f):
  cache = {}
  def memoized(*arg):
    if arg in cache:
      return cache[arg]
    result = f(*arg)
    cache[arg] = result
    return result
  return memoized

PADDING = (0, 0, 0, 0)

def non_empty(row):
  return tuple(cell for cell in row if cell>0)

def _crunch(row):
  if len(row)<=1: return row
  if row[0] == row[1]:
    return crunch((row[0] + row[1],) + row[2:])
  crunched = crunch(row[1:])
  if row[0] == crunched[0]:
    return crunch((row[0] + crunched[0],) + crunched[1:])
  return row[:1] + crunched

crunch = memoize(_crunch)

def pad(row):
  return (row + PADDING)[:4]

def left(board):
  return tuple(row_left(row) for row in board)

def row_left(row):
  return pad(crunch(non_empty(row)))

def right(board):
  return tuple(row_right(row) for row in board)

def row_right(row):
  return tuple(reversed(row_left(tuple(reversed(row)))))

def up(board):
  return transpose(left(transpose(board)))

def down(board):
  return transpose(right(transpose(board)))

directions = (left, right, up, down)

def transpose(board):
  return tuple(tuple(row[i] for row in board) for i in range(0, 4))

def score(board):
  return sum(sum(1 for cell in row if cell==0) for row in board)

def replace(tup, i, v):
  return tup[:i] + (v,) + tup[i+1:]

def futures(board):
  for i in range(0, 4):
    row = board[i]
    for j in range(0, 4):
      if row[j] == 0:
        yield replace(board, i, replace(row, j, 2))

def best_score(board, depth):
  if depth==0:
    return max(score(direction(board)) for direction in directions)
  return max(score(best_move(direction(board), depth - 1))
             for direction in directions)

def avg(iter):
  itemCount = 0
  sum = 0.0
  for i in iter:
    itemCount += 1
    sum += i
  return sum / itemCount

def choose_multiple(count, seq):
  bag = list(range(0, len(seq)))
  chosen = []
  for i in range(0, min(count, len(seq))):
    choice = random.choice(bag)
    bag.remove(choice)
    chosen.append(choice)
  return [seq[choice] for choice in chosen]

def avg_future(board, depth):
  random_futures = choose_multiple(2 + (depth * 2), tuple(futures(board)))
  return avg(best_score(future, depth) for future in random_futures)

def _best_move(board, depth):
  moved_boards = (direction(board) for direction in directions)
  new_boards = tuple(m for m in moved_boards if m!=board)
  if len(new_boards)==0: return board
  scores = tuple(avg_future(new_board, depth) for new_board in new_boards)
  max_score = max(scores)
  for i in range(len(new_boards)):
    if scores[i]==max_score: return new_boards[i]
best_move = memoize(_best_move)

def random_future(board):
  all_futures = tuple(futures(board))
  if len(all_futures)==0: return board
  return random.choice(all_futures)

def do_move(board, depth):
  return random_future(best_move(board, depth))

def show(board):
  print
  for row in board:
    print row

EMPTY_BOARD = (
  (0, 0, 0, 0),
  (0, 0, 0, 0),
  (0, 0, 0, 0),
  (0, 0, 0, 0))

state = random_future(random_future(EMPTY_BOARD))
while 1:
  show(state)
  new_state = do_move(state, 1)
  if new_state == state: exit(0)
  state = new_state
