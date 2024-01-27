import pandas
import csv


class KPIUnit:
    __slots__ = ('id', 'name')

    def __init__(self, id: str, name: str) -> None:
        self.id = id
        self.name = name


class KPIEnvScore:
    __slots__ = ('kpi_id', 'score')

    def __init__(self, kpiId: float, score: float) -> None:
        self.kpi_id = int(kpiId)
        self.score = score


class KPIHumanScore:
    __slots__ = ('kpi_id', 'score', 'human_id')

    def __init__(self, kpiId: float, score: float, humanId: float) -> None:
        self.kpi_id = int(kpiId)
        self.score = score
        self.human_id = int(humanId)


def get_kpi_weight_matrix(filename: str = 'KpiWeight.csv'):
    matrix_dict = {}

    with open(filename, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        next(csv_reader, None)
        for row in csv_reader:
            kpi_id = row[0]
            values = [float(value) for value in row[1:]]
            matrix_dict[kpi_id] = values
    return matrix_dict

def get_list_KPI_env_score(filename: str = 'KPIEnvScore.csv') -> list:
    df = pandas.read_csv(filename)
    return [KPIEnvScore(row[1]['kpi_id'], row[1]['score']) for row in df.iterrows()]


def get_list_KPI_unit(filename: str = 'KpiUnit.csv') -> list:
    df = pandas.read_csv(filename)
    kpi_unit_list = df.apply(lambda row: KPIUnit(
        row['kpi_id'], row['name']), axis=1).tolist()

    kpi_unit_list.extend([KPIUnit('start', 'Start kpi'), KPIUnit(
        'finish', 'Finish kpi')])

    return kpi_unit_list


def get_list_KPI_human_score(filename: str = 'KpiHumanScore.csv') -> list:
    df = pandas.read_csv(filename)
    return [KPIHumanScore(row[1]['kpi_id'], row[1]['score'], row[1]['human_id']) for row in df.iterrows()]


def get_index_by_kpi_id_in_file(filename: str = 'KpiWeight.csv', kpi_id='start') -> int:
    df = pandas.read_csv(filename, index_col='kpi_id')

    try:
        index = df.index.get_loc(kpi_id)
    except KeyError:
        index = -1

    return index
