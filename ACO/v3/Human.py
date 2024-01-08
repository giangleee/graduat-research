import pandas


class Human:
    __slots__ = ('id', 'name', 'score')

    def __init__(self, id, name, score) -> None:
        self.id = id
        self.name = name
        self.score = score


def get_list_human() -> list:
    df = pandas.read_csv('./HumanAbilityScore.csv')
    return [Human(index, row['human'], row['score'])
            for index, row in df.iterrows()]
