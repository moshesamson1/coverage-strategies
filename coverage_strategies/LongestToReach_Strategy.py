import operator
from math import fabs
from coverage_strategies.coverage_strategies.Entities import Slot, Strategy, Agent, Board


def assign_level_to_slots(board:Board, init:Slot):
    leveled_vertices = {}

    # Mark all the vertices as not visited
    visited = {i: False for j in board.Slots for i in j}
    queue = [(init, 0)]
    visited[init] = True
    while queue:
        s, l = queue.pop(0)
        leveled_vertices[s] = l

        # Get all adjacent vertices of the
        # dequeued vertex s. If a adjacent
        # has not been visited, then mark it
        # visited and enqueue it.
        # all unvisited neighbors get level value of +1 of the current level value
        for i in [i for i in s.get_8_inbound_neighbors(board)]:
            if not visited[i]:
                queue.append((i, l + 1))
                visited[i] = True

    return leveled_vertices


def cover_current_level(level, current:Slot, board:Board, leveled_slots):
    slots = [current]
    current_slot = current
    level_amount = len([i for i in leveled_slots.values() if i==level])

    leveled_neighbors = lambda slot: [i for i in current_slot.get_inbound_neighbors(board) if leveled_slots[i] == level]
    nonpresent_leveled_neighbors = lambda slot,l: [i for i in leveled_neighbors(slot) if i not in l]

    # go toward a neighbor of the same level, covering until having a single neighbor with level value
    uncovered_inbound_neighbors = nonpresent_leveled_neighbors(current_slot, slots)
    while uncovered_inbound_neighbors:
        current_slot = uncovered_inbound_neighbors.pop()
        slots.append(current_slot)
        uncovered_inbound_neighbors = nonpresent_leveled_neighbors(current_slot, slots)

    # if not covered all of this level, go the the opposite direction and cover until all level is covered
    doubly_covered_slots = []
    while len(set(slots)) < level_amount:
        uncovered_leveled_slots = nonpresent_leveled_neighbors(current_slot, doubly_covered_slots)
        if not uncovered_leveled_slots:
            break

        current_slot = uncovered_leveled_slots[0]
        doubly_covered_slots.append(current_slot)
        slots.append(current_slot)

    return slots[1:]


class LongestToReach_Strategy(Strategy):
    def get_steps(self, agent_r:Agent, board_size = 50, agent_o:Agent = None):
        assert agent_o is not None

        # 1. perform bfs and set LEVEL values
        # 2. go to cell with highest LEVEL value
        # 3. while not all cells covered:
        #   3.1. cover current LEVEL
        #   3.2. if next level adjacent, go there
        #   3.3  if not all cells are covered, go to next level (search)

        covered_slots = []

        # 1. perform bfs
        board = agent_o.gameBoard
        leveled_slots = assign_level_to_slots(board, Slot(agent_o.InitPosX, agent_o.InitPosY))
        #
        distance = lambda a,b: fabs(a.row-b.row)+fabs(a.col-b.col)
        edges_and_distance_score = lambda slot: len(slot.get_inbound_neighbors(board))*10 + distance(slot,Slot(agent_r.InitPosX, agent_r.InitPosY))
        # s = sorted(leveled_slots.items(), key=edges_and_distance_score)

        max_level = max(leveled_slots.values())
        max_leveled_slots = [i for i in leveled_slots if leveled_slots[i]==max_level]
        ordered_max_leveled_slots = sorted(max_leveled_slots, key=edges_and_distance_score)

        # 2. go to cell with highest LEVEL value
        # max_level_slot = max(leveled_slots.items(), key=operator.itemgetter(1))
        best_max_level_slot = ordered_max_leveled_slots[0]
        path_to_max_slot = Strategy.go_from_a_to_b(
            a=Slot(agent_r.InitPosX, agent_r.InitPosY),
            b=best_max_level_slot)
        self.steps.extend(path_to_max_slot)
        current_slot = best_max_level_slot
        covered_slots.append(current_slot)
        # covered_slots.extend(path_to_max_slot)

        # 3. while not all cells covered:
        while len(set(self.steps)) < board.Rows*board.Cols:
            #   3.1. cover current LEVEL
            level_steps = cover_current_level(level=leveled_slots[current_slot],current=current_slot, board=board, leveled_slots=leveled_slots)
            self.steps.extend(level_steps)
            covered_slots.extend(level_steps)

            if level_steps:
                current_slot = level_steps[-1]

            can_repeat = lambda x:x

            #   3.2. if next level adjacent, go there
            preferred_n = Slot(-1,-1)
            for n in current_slot.get_inbound_neighbors(board):

                if n not in covered_slots and leveled_slots[n] == leveled_slots[current_slot]-1:
                    if preferred_n == Slot(-1,-1) or len(n.get_inbound_neighbors(board)) < len(preferred_n.get_inbound_neighbors(board)):
                        preferred_n = n

            if preferred_n is not Slot(-1,-1):
                current_slot = preferred_n
                covered_slots.append(current_slot)
                self.steps.append(current_slot)
                # break
            else:
                pass
            #   3.3  if next level not adjacent, and process not finished, search for next level (higher than 0) and go there

        return self.steps