import operator

from coverage_strategies.coverage_strategies.Entities import Slot, Strategy, Agent, Board


def assign_level_to_slots(board:Board, init:Slot):
    leveled_vertices = {}

    # Mark all the vertices as not visited
    visited = {i: False for j in board.Slots for i in j}
    queue = []
    queue.append((init, 0))
    visited[init] = True
    while queue:
        s, l = queue.pop(0)
        leveled_vertices[s] = l

        # Get all adjacent vertices of the
        # dequeued vertex s. If a adjacent
        # has not been visited, then mark it
        # visited and enqueue it.
        # all unvisited neighbors get level value of +1 of the current level value
        for i in [i for i in [s.go_south(), s.go_east(), s.go_west(), s.go_north()] if i.in_bounds(board)]:
            if not visited[i]:
                queue.append((i, l + 1))
                visited[i] = True

    return leveled_vertices


class LongestToReach_Strategy(Strategy):
    def get_steps(self, agent_r:Agent, board_size = 50, agent_o:Agent = None):
        assert agent_o is not None

        # 1. perform bfs and set LEVEL values
        # 2. go to cell with highest LEVEL value
        # 3. while not all cells covered:
        #   3.1. cover current LEVEL
        #   3.2. if next level adjacent, go there
        #   3.3  if not all cells are covered, go to next level (search)

        # 1. perform bfs
        board = agent_o.gameBoard
        leveled_slots = assign_level_to_slots(board, Slot(agent_o.InitPosX, agent_o.InitPosY))

        # 2. go to cell with highest LEVEL value
        max_level_slot = max(leveled_slots.items(), key=operator.itemgetter(1))[0]
        self.steps.extend(Strategy.go_from_a_to_b(
            a=Slot(agent_r.InitPosX, agent_r.InitPosY),
            b=max_level_slot)
        )
        print(1)

        #
        # # go to the farthest corner
        # self.steps.extend(Strategy.go_from_a_to_b(a=Slot(agent_r.InitPosX, agent_r.InitPosY),
        #                                           b=Strategy.get_farthest_corner(
        #                                               a=Slot(agent_o.InitPosX, agent_o.InitPosY),
        #                                               board_size=32)))
        #
        # # from there, cover semi-cyclic
        # current_slot = self.steps[-1]
        # v_dir = 'u' if current_slot.row == board_size - 1 else 'd'
        # h_dir = 'r' if current_slot.col == board_size - 1 else 'l'
        # start_vertical = True
        # distance = 1
        # counter = 1
        #
        # # initial horizontal step
        # current_slot = current_slot.go_west() if h_dir == 'r' else current_slot.go_east()
        # self.steps.append(current_slot)
        # counter += 1
        #
        # while counter <= board_size * board_size and distance < board_size:
        #     if start_vertical:
        #         # going vertically
        #         for _ in range(distance):
        #             current_slot = current_slot.go_north() if v_dir == 'u' else current_slot.go_south()
        #             self.steps.append(current_slot)
        #             counter += 1
        #
        #         # going horizontally
        #         for _ in range(distance):
        #             current_slot = current_slot.go_west() if h_dir == 'l' else current_slot.go_east()
        #             self.steps.append(current_slot)
        #             counter += 1
        #
        #         # final vertical step
        #         if counter < board_size * board_size:
        #             current_slot = current_slot.go_north() if v_dir == 'u' else current_slot.go_south()
        #             self.steps.append(current_slot)
        #             counter += 1
        #
        #     else:
        #         # going horizontally
        #         for _ in range(distance):
        #             current_slot = current_slot.go_west() if h_dir == 'l' else current_slot.go_east()
        #             self.steps.append(current_slot)
        #             counter += 1
        #
        #         # going vertically
        #         for _ in range(distance):
        #             current_slot = current_slot.go_north() if v_dir == 'u' else current_slot.go_south()
        #             self.steps.append(current_slot)
        #             counter += 1
        #
        #         # final horizontal step
        #         if counter < board_size * board_size:
        #             current_slot = current_slot.go_west() if h_dir == 'l' else current_slot.go_east()
        #             self.steps.append(current_slot)
        #             counter += 1
        #
        #     start_vertical = not start_vertical
        #     h_dir = 'r' if h_dir == 'l' else 'l'
        #     v_dir = 'u' if v_dir == 'd' else 'd'
        #
        #     distance += 1
        #
        return self.steps