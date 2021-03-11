from coverage_strategies.Entities import Board, Agent, StrategyEnum, Game, Slot

def run_game(pos_r:Slot, pos_o:Slot, w=32, h=32):
    b = Board(w, h)
    agentO = Agent("O", StrategyEnum.RandomSTC, pos_o.row, pos_o.col, board=b)
    agentR = Agent("R", StrategyEnum.LONGEST_TO_REACH, pos_r.row, pos_r.col, board=b, agent_o=agentO)
    g = Game(agent_o=agentO, agent_r=agentR, size=(w, h))
    rg, _ = g.run_game()


def test_positions(positions):
    ir=Slot(positions[0][0], positions[0][1])
    io=Slot(positions[1][0], positions[1][1])
    run_game(ir, io)


