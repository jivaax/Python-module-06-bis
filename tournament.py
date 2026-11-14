from ex3 import (
    CreatureFactory,
    FlameFactory,
    TransformCreatureFactory
)

from ex4 import (
    BattleStrategy,
    NormalStrategy,
    AggressiveStrategy,
    InvalidStrategyError
)


def battle(
    opponents: list[tuple[CreatureFactory, BattleStrategy]]
) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")

    creatures = [
        (factory.create_base(), strategy)
        for factory, strategy in opponents
    ]

    for i in range(len(creatures)):
        for j in range(i + 1, len(creatures)):
            first, first_strategy = creatures[i]
            second, second_strategy = creatures[j]

            print("\n* Battle *")
            print(first.describe())
            print(" vs.")
            print(second.describe())
            print(" now fight!")

            try:
                first_strategy.act(first)
                second_strategy.act(second)
            except InvalidStrategyError as e:
                print(f"Battle error, aborting tournament: {e}")
                return


if __name__ == "__main__":
    flame_factory = FlameFactory()
    transform_factory = TransformCreatureFactory()

    normal = NormalStrategy()
    aggressive = AggressiveStrategy()

    print("Tournament 0 (basic)")
    print(" [ (Flameling+Normal), (Shiftling+Aggressive) ]")

    opponents_0: list[tuple[CreatureFactory, BattleStrategy]] = [
        (flame_factory, normal),
        (transform_factory, aggressive)
    ]

    battle(opponents_0)

    print("\nTournament 1 (error)")
    print(" [ (Shiftling+Aggressive), (Flameling+Aggressive) ]")

    opponents_1: list[tuple[CreatureFactory, BattleStrategy]] = [
        (transform_factory, aggressive),
        (flame_factory, aggressive)
    ]

    battle(opponents_1)
