import pandas
import csv


class KPIUnit:
    __slots__ = ('__id', '__name')

    def __init__(self, id: int, name: str) -> None:
        self.__id = id
        self.__name = name


class KPIEnvScore:
    __slots__ = ('id', 'kpi_id', 'score')

    def __init__(self, id: int, kpiId: int, score: float) -> None:
        self.id = id
        self.kpi_id = kpiId
        self.score = score


class KPIHumanScore:
    __slots__ = ('id', 'kpi_id', 'score', 'human_id')

    def __init__(self, id: int, kpiId: int, score: float, humanId: str) -> None:
        self.id = id
        self.kpi_id = kpiId
        self.score = score
        self.human_id = humanId


def get_kpi_weight_matrix(filename: str = 'KpiWeight.csv'):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        matrix = [
            [int(row[key]) for key in row if key != 'KPI']
            for row in reader
        ]
    return matrix


def get_list_KPI_env_score() -> list:
    df = pandas.read_csv('./KPIEnvScore.csv')
    return [KPIEnvScore(index, row['KPI'], row['score']) for index, row, in df.iterrows()]


def get_list_KPI_unit() -> list:
    df = pandas.read_csv('./KpiUnit.csv')
    return [KPIUnit(index, row['name']) for index, row in df.iterrows()]


def get_list_KPI_human_score() -> list:
    df = pandas.read_csv('./KpiHumanScore.csv')
    return [KPIHumanScore(index, row['KPI'], row['score'], row['human']) for index, row in df.iterrows()]
