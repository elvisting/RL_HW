# Adapted from: https://github.com/lazyprogrammer/machine_learning_examples/tree/master/rl
import numpy as np

class Grid: # Environment
  def __init__(self, width, height, start, noise_prob=0):
    self.width = width
    self.height = height
    self.i = start[0]
    self.j = start[1]
    self.noise_prob = noise_prob

  def set(self, rewards, actions):
    # rewards should be a dict of: (i, j): r (row, col): reward
    # actions should be a dict of: (i, j): A (row, col): list of possible actions
    self.rewards = rewards
    self.actions = actions

  def set_state(self, s):
    self.i = s[0]
    self.j = s[1]

  def current_state(self):
    return (self.i, self.j)

  def is_terminal(self, s):
    return s not in self.actions

  def move(self, action):
    
    # with a probability of noise_prob, do a random action:
    if np.random.uniform() < self.noise_prob:
      action = np.random.choice(self.actions[(self.i, self.j)])
        
    # check if legal move first
    if action in self.actions[(self.i, self.j)]:              
      if action == 'U':
        self.i -= 1
      elif action == 'D':
        self.i += 1
      elif action == 'R':
        self.j += 1
      elif action == 'L':
        self.j -= 1
        
    # return a reward (if any)
    return self.rewards.get((self.i, self.j), 0)

  def undo_move(self, action):
    # these are the opposite of what U/D/L/R should normally do
    if action == 'U':
      self.i += 1
    elif action == 'D':
      self.i -= 1
    elif action == 'R':
      self.j -= 1
    elif action == 'L':
      self.j += 1
    # raise an exception if we arrive somewhere we shouldn't be
    # should never happen
    assert(self.current_state() in self.all_states())

  def game_over(self):
    # returns true if game is over, else false
    # true if we are in a state where no actions are possible
    return (self.i, self.j) not in self.actions

  def all_states(self):
    # possibly buggy but simple way to get all states
    # either a position that has possible next actions
    # or a position that yields a reward
    return set(self.actions.keys()) | set(self.rewards.keys())


def standard_grid(noise_prob=0.1):
  # define a grid that describes the reward for arriving at each state
  # and possible actions at each state
  # the grid looks like this
  # x means you can't go there
  # s means start position
  # number means reward at that state
  # .  .  .  1
  # .  x  . -1
  # s  .  .  .
  g = Grid(3, 4, (2, 0), noise_prob=noise_prob)
  rewards = {(0, 3): 1.1, (1, 3): -1}
  actions = {
    (0, 0): ('D', 'R'),
    (0, 1): ('L', 'R'),
    (0, 2): ('L', 'D', 'R'),
    (1, 0): ('U', 'D'),
    (1, 2): ('U', 'D', 'R'),
    (2, 0): ('U', 'R'),
    (2, 1): ('L', 'R'),
    (2, 2): ('L', 'R', 'U'),
    (2, 3): ('L', 'U'),
  }
  g.set(rewards, actions)
  return g


def negative_grid(step_cost=-0.1):
  # in this game we want to try to minimize the number of moves
  # so we will penalize every move
  g = standard_grid()
  g.rewards.update({
    (0, 0): step_cost,
    (0, 1): step_cost,
    (0, 2): step_cost,
    (1, 0): step_cost,
    (1, 2): step_cost,
    (2, 0): step_cost,
    (2, 1): step_cost,
    (2, 2): step_cost,
    (2, 3): step_cost,
  })
  return g
  
def grid_5x5(step_cost=-0.1):
  g = Grid(5, 5, (4, 0))
  rewards = {(0, 4): 1, (1, 4): -1}
  actions = {
    (0, 0): ('D', 'R'),
    (0, 1): ('L', 'R'),
    (0, 2): ('L', 'R'),
    (0, 3): ('L', 'D', 'R'),
    (1, 0): ('U', 'D', 'R'),
    (1, 1): ('U', 'D', 'L'),
    (1, 3): ('U', 'D', 'R'),
    (2, 0): ('U', 'D', 'R'),
    (2, 1): ('U', 'L', 'R'),
    (2, 2): ('L', 'R', 'D'),
    (2, 3): ('L', 'R', 'U'),
    (2, 4): ('L', 'U', 'D'),
    (3, 0): ('U', 'D'),
    (3, 2): ('U', 'D'),
    (3, 4): ('U', 'D'),
    (4, 0): ('U', 'R'),
    (4, 1): ('L', 'R'),
    (4, 2): ('L', 'R', 'U'),
    (4, 3): ('L', 'R'),
    (4, 4): ('L', 'U'),
  }
  g.set(rewards, actions)

  # non-terminal states
  visitable_states = actions.keys()
  for s in visitable_states:
    g.rewards[s] = step_cost

  return g

def print_values(V, g):
  for i in range(g.width):
    print("---------------------------")
    for j in range(g.height):
      v = V.get((i,j), 0)
      if v >= 0:
        print(" %.2f|" % v, end="")
      else:
        print("%.2f|" % v, end="") # -ve sign takes up an extra space
    print("")


def print_policy(P, g):
  for i in range(g.width):
    print("---------------------------")
    for j in range(g.height):
      a = P.get((i,j), ' ')
      if a == ' ':
        print(" N/A |", end="")    
      else:  
        print("  %s  |" % a, end="")
    print("")
