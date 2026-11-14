from abc import ABC, abstractmethod
from ex3.creatures import Creature, TransformCapability


class InvalidStrategyError(Exception):
    pass


class BattleStrategy(ABC):
    @abstractmethod
    def is_valid(self, entity: Creature) -> bool:
        pass

    @abstractmethod
    def act(self, entity: Creature) -> None:
        pass


class NormalStrategy(BattleStrategy):
    def is_valid(self, entity: Creature) -> bool:
        return isinstance(entity, Creature)

    def act(self, entity: Creature) -> None:
        if not self.is_valid(entity):
            raise InvalidStrategyError(
                f"Invalid Creature '{entity.name}' "
                "for this normal strategy"
            )

        print(entity.attack())


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, entity: Creature) -> bool:
        return isinstance(entity, TransformCapability)

    def act(self, entity: Creature) -> None:
        if not self.is_valid(entity):
            raise InvalidStrategyError(
                f"Invalid Creature '{entity.name}' "
                "for this aggressive strategy"
            )

        if isinstance(entity, TransformCapability):
            print(entity.transform())
            try:
                print(entity.attack())
            finally:
                print(entity.revert())
