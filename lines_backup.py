# Given the total number of lines in the game and the maximum number of adjacent lines you're allowed to cross off in a single go,
# moves_list() returns a complete list of the possible moves in the game (given as tuples).
def moves_list(total,max):
  # total : total number of lines in the game
  # max : maximum number of adjacent lines that can be crossed off in a go
  moves = []
  # Need to iterate over number of adjacent lines and line number
  for num_adj_lines in range(1,max + 1):
    for line_num in range(1,total+1):
      if line_num + num_adj_lines -1 <= total:
        # Add the tuple (line_num, .. , line_num + num_adj_lines - 1) to the list 'moves'
        # First create it as a list and then use the 'tuple' function to convert it
        move_as_list = []
        for num in range(line_num, line_num + num_adj_lines):
          move_as_list.append(num)
        move = tuple(move_as_list)
        moves.append(move)
        
  return moves

# Now I need a function that, when given the total list of remaining moves in the game and the move being taken, returns a new list 
# of the remaining moves
def take_turn(moves,move_taken):
  # 'moves' is a list of tuples
  # 'move_taken' is a tuple
  # Idea is that we go through the elements of 'move_taken' in turn and remove any tuples containing those elements from 'moves'.
  # Have found it's pretty treacherous to have a functionn that edits the arguments it takes (especially when function is used in recursion),
  # so it seems important to make a copy and use that instead of the original
  moves_copy = moves[:]
  for move in moves_copy[:]:  # here I'm iterating over a copy of moves rather than moves itself, as moves itself is being modified by the iteration
    for num in move_taken:
      if num in move: # Remove move from moves
        moves_copy.remove(move)
        break  # No point checking if other elements of move_taken are in 'move' since we've now removed it from the moves list
  
  return moves_copy


def list_games(moves_list):
  # Returns a list of lists, each list is a game
  remaining_moves = moves_list[:]
  if len(remaining_moves) <= 1:
    list_of_games = [ remaining_moves ]
    return list_of_games
  else:
    list_of_games = []
    # Here we use recursion.
    # We know that if we only have 1 (or 0) moves in a game, the total list of games is simply that one element.
    # Now imagine we have a list [a, b, c, ..., n] of moves, and that the list [X, Y, Z, ..., Mx] are the remaining moves having taken move 'x'.
    # Since this is a reduced list and finite, we assume we can calculate the total list of games for the remaining moves list, [G1, G2, ..., Gxv]
    # Then the total list of games is [[a]+G1, [a]+G2, ..., [a]+Gav, [b]+G1, [b]+G2, ..., [b]+Gbv, ... [n]+Gnv] - don't quite have the right subscripts
    # here!  But hopefully you can see that, if in a trivial case we can work out a list and in a general case we can reduce it to something simply, we
    # can eventually get there.
    for move in remaining_moves:
      for game in list_games(take_turn(remaining_moves,move)):
        new_list = [ move ]
        new_list.extend(game)
        list_of_games.append(new_list)
      
  return list_of_games
 
def give_partition(moves_list):
# Imagine we have two games in the following state (X is a crossed line, I is an uncrossed line)
# Game 1 is currently:   X X I X I I I X X I X X
# Game 2 is currently:   I X I X I I I
# These games are equivalent and can be completely described by their partitions, which I'm defining as a list of lengths of the sets of 
# adjacent lines, ordered from smallest to largest.  So their partition is [ 1, 1, 3 ]
# I want a function that will take a moves list and return the partition, so we can easily see if two games are equivalent.
  partition = []
  single_lines = []
  length = 0
  # First step - make a list of the available single moves
  for move in sorted(moves_list):
    if len(move) == 1: single_lines.append(move[0])
  # Go from the bottom one to the top one computing lengths of the partition bits
  # I actually go from bottom one to top one +1, since I only add in a partition bit when I reach a number that's not in the single_lines list,
  # and the top number might be in!  (It looks like +2 below, but remember range[1,4] gives [1,2,3])  
  for num in range(single_lines[0],single_lines[-1]+2):
    if num in single_lines: length = length + 1
    else:
      # num not in the list of available single lines means we have reached the end of part of the partition (add it) or not yet
      # started one (ie. the previous num hadn't been in the set of single lines either)
      if length != 0:
        partition.append(length)
        length = 0
  return sorted(partition)

# Should be able to use the partitions idea to have a much more efficient way of calculating possible games.
# Rather than a list of moves, I could specify a game ('up to symmetry') by a list of partitions
# The only extra information we need is the maximum number of adjacent lines you're allowed to cross off in one go
# Will be interesting to find out how many different games there reeeaaally are for a given moves list
# You guessed it - I now want a function that does that ...

# First, a function to do a special case - when we're crossing off a fixed number of lines from a fixed set of adjacent lines
def poss_partitions_special(total_adj_lines,crossed_lines):
  # total_adj_lines is just the number of lines
  # crossed_lines is the number of lines we're intending to cross
  if total_adj_lines < crossed_lines:
    return -1  # since you can't cross off more lines than you have
  if total_adj_lines == crossed_lines:
    return []  # There is no partition if you cross off all the lines you have  
  partitions = []
  i = 0
  for i in range(1,total_adj_lines + 1 - crossed_lines):  # Don't have to go all the way along - just need to think what upper limit should be
    j = i + crossed_lines -1  # j is the top line of the set of adjacent lines you're crossing off
    new_partition = [i-1, total_adj_lines - j]
    if 0 in new_partition:
      new_partition.remove(0)
    partitions.append(sorted(new_partition))
  
  # Now we want to ensure the entries are unique, so we sort them and go through the list, checking at each point that the next entry isn't the same
  # If it is, we remove the current entry
  sorted_partitions = sorted(partitions)
  for entry in sorted_partitions[:-2]:   # Rem: don't iterate over something you're modifying, and no point looking at the last
                                         # entry as there's nothing after it that it might be a duplicate of
    if sorted_partitions[sorted_partitions.index(entry) + 1] == entry:
      sorted_partitions.remove(entry)  # remove duplicated entries from partitions
  return sorted_partitions

def poss_partitions(partition,max_adj_lines):
  # ok, given a partition, what are the possible partitions when we can cross off up to max_adj_lines adjacent lines?
  partitions_list = []
  for adj_lines in range(1, max_adj_lines + 1):
    # Create a new list, entries a subset of partitions, where entries are unique and >= adj_lines
    unique_entries = []
    for entry in partition:
      if entry >= adj_lines and entry not in unique_entries: unique_entries.append(entry)
    for entry in unique_entries:
      copy = partition[:]
      copy.remove(entry)  # Remove the set of adjacent lines we're splitting by crossing some lines in it ...
      if len(poss_partitions_special(entry,adj_lines)) > 0:  # remember that if nothing is returned, we haven't split a set of adjacent lines 
                                                             # into two - we've actually crossed the whole set off.
        for element in poss_partitions_special(entry,adj_lines):   # each element is a possible new bit of the partition
          new_copy = copy[:]
          new_copy.extend(element)   # now new_copy is our old partition without the set of adjacent lines we split up by crossing
                                     # some off and but with the resulting new bits due to that move
          # Currently I'm missing the cases when poss_partitions_special returns the empty list
          partitions_list.append(sorted(new_copy))
      else:
        partitions_list.append(copy)
  return sorted(partitions_list)
