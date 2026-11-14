from ex3 import TransformCreatureFactory
from ex3.creatures import Creature, TransformCapability


def test_transformation(entity: Creature) -> None:
    if not isinstance(entity, TransformCapability):
        print("This creature cannot transform.")
        return

    print(entity.describe())
    print(entity.attack())
    print(entity.transform())
    print(entity.attack())
    print(entity.revert())


if __name__ == "__main__":
    print("Testing Creature with transform capability")

    factory = TransformCreatureFactory()

    base = factory.create_base()
    evolved = factory.create_evolved()

    print(" base:")
    test_transformation(base)

    print(" evolved:")
    test_transformation(evolved)
