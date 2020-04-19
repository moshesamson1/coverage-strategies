
from coverage_strategies.Strategies import VerticalCircularCoverage_Strategy, HorizontalCircularCoverage_Strategy, \
    TrulyRandomStrategy, LongestToReach_Strategy, LCP_Strategy, CircleOutsideFromIo_Strategy, \
    CircleOutsideFromCornerFarthestFromIo_Strategy, VerticalCoverageFromCornerFarthestFromIo_Strategy, \
    CircleOutsideFromBoardCenter_Strategy, CircleInsideFromCornerFarthestFromIo_Strategy, \
    VerticalNonCircularCoverage_Strategy, STC_Strategy, CoverByQuarters_Strategy, InterceptThenCopy_Strategy, \
    CircleOutsideFromCornerAdjacentToIo_Strategy

from coverage_strategies.Entities import StrategyEnum

def get_strategy_from_enum(strategy_enum: StrategyEnum):
    if strategy_enum == StrategyEnum.VerticalCoverageCircular:
        return VerticalCircularCoverage_Strategy()
    elif strategy_enum == StrategyEnum.HorizontalCoverageCircular:
        return HorizontalCircularCoverage_Strategy()
    elif strategy_enum == StrategyEnum.FullKnowledgeInterceptionCircular:
        return InterceptThenCopy_Strategy()
    elif strategy_enum == StrategyEnum.QuartersCoverageCircular:
        return CoverByQuarters_Strategy()
    elif strategy_enum == StrategyEnum.RandomSTC:
        return STC_Strategy()
    elif strategy_enum == StrategyEnum.VerticalCoverageNonCircular:
        return VerticalNonCircularCoverage_Strategy()
    elif strategy_enum == StrategyEnum.SpiralingIn:
        return CircleInsideFromCornerFarthestFromIo_Strategy()
    elif strategy_enum == StrategyEnum.SpiralingOut:
        return CircleOutsideFromBoardCenter_Strategy()
    elif strategy_enum == StrategyEnum.VerticalFromFarthestCorner_OpponentAware:
        return VerticalCoverageFromCornerFarthestFromIo_Strategy()
    elif strategy_enum == StrategyEnum.SemiCyclingFromFarthestCorner_OpponentAware:
        return CircleOutsideFromCornerFarthestFromIo_Strategy()
    elif strategy_enum == StrategyEnum.SemiCyclingFromAdjacentCorner_col_OpponentAware:
        return CircleOutsideFromCornerAdjacentToIo_Strategy.CircleOutsideFromCornerAdjacentToIo_Strategy(False)
    elif strategy_enum == StrategyEnum.SemiCyclingFromAdjacentCorner_row_OpponentAware:
        return CircleOutsideFromCornerAdjacentToIo_Strategy.CircleOutsideFromCornerAdjacentToIo_Strategy(True)
    elif strategy_enum == StrategyEnum.CircleOutsideFromIo:
        return CircleOutsideFromIo_Strategy()
    elif strategy_enum == StrategyEnum.LCP:
        return LCP_Strategy()
    elif strategy_enum == StrategyEnum.LONGEST_TO_REACH:
        return LongestToReach_Strategy()
    elif strategy_enum == StrategyEnum.TRULY_RANDOM:
        return TrulyRandomStrategy()