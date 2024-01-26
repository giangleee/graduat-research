import pandas


class Human:
    __slots__ = ('id', 'name', 'ability_score')

    def __init__(self, id: float, name: str, abilityScore: float) -> None:
        self.id = int(id)
        self.name = name
        self.ability_score = abilityScore


def get_list_human(filename: str = 'HumanAbilityScore.csv') -> list:
    df = pandas.read_csv(filename)
    return [Human(row[1]['human_id'], row[1]['name'], row[1]['abilityScore'])
            for row in df.iterrows()]
