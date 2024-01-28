// Import necessary libraries and modules (assumed equivalent modules are available in JS)
// const { getKpiWeightMatrix, getListKPIUnit, getListKPIEnvScore, getListKPIHumanScore, getIndexByKpiIdInFile, KPIUnit } = require('./KPI');
import * as KPI from './KPI.js';
import * as Human from './Human.js'

const {
    getKpiWeightMatrix,
    getListKPIUnit,
    getListKPIEnvScore,
    getListKPIHumanScore,
    getIndexByKpiIdInFile,
    KPIUnit
} = KPI;
// const { getListHuman } = require('./Human');
const { getListHuman } = Human;

// Define constants
const START_POINT_VALUE = 'start';
const FINISH_POINT_VALUE = 'finish';

// Function to build a matrix
function buildMatrix(numPoint, matrixDisc) {
    // const matrix = Array.from({ length: numPoint }, () => Array(numPoint).fill(0.0));
    // // console.log(matrixDisc)

    // Object.keys(matrixDisc).forEach((key, i) => {
    //     console.log(matrixDisc[key])
    //     // matrix[i] = matrixDisc[key].map(value => value > 0);
    // });

    // return matrix;
    const matrix = [
        [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0],
        [0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        [0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0],
        [0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0],
        [0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0],
        [0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    ];
    return matrix
}
function getKeyByIndex(obj, index) {
  const keysArray = Object.keys(obj);
  return keysArray[index] || null;
}

class AntSystemOptimization {
    constructor(generation, population, beta = 2, ro = 0.4) {
        this.list_kpi_unit = getListKPIUnit();
        this.weight_matrix = getKpiWeightMatrix();
        this.kpi_env_score = getListKPIEnvScore();
        this.human_ability_score = getListHuman();
        this.kpi_human_score = getListKPIHumanScore();
        this.default_pheromone_tao_matrix = buildMatrix(this.weight_matrix[START_POINT_VALUE].length, this.weight_matrix);
        this.pheromone_tao_matrix = [...this.default_pheromone_tao_matrix.map(row => [...row])];
        this.generation = generation;
        this.population = population;
        this.beta = beta;
        this.ro = ro;
        this.best_path = [];
        this.best_path_length = 0;
    }

    getHumanProbabilisticBaseKpi(humanId, endPointId) {
        const matchingItems = this.kpi_human_score.filter(item => item.human_id === humanId && endPointId === String(item.kpi_id));
        return matchingItems.length ? matchingItems[0].score : 0.0;
    }

    getListAvailableNextPoint(startPoint, currentAntPath) {
        const convertStartPoint = startPoint !== START_POINT_VALUE && startPoint !== FINISH_POINT_VALUE ? String(parseInt(startPoint)) : startPoint;

        const reachablePoints = this.weight_matrix[convertStartPoint].reduce((acc, value, index) => {
            if (value > 0 && !currentAntPath.includes(getKeyByIndex(this.weight_matrix, index))) {
                acc.push(getKeyByIndex(this.weight_matrix, index));
            }
            return acc;
        }, []);

        return reachablePoints;
    }

    getEtaValue(startPoint, endPointIndex) {
        return 1 / this.weight_matrix[startPoint][endPointIndex];
    }

    equationValue(startPoint, endPoint) {
        const indexStartPoint = getIndexByKpiIdInFile({ kpi_id: startPoint });
        const indexEndPoint = getIndexByKpiIdInFile({ kpi_id: endPoint });
        return this.pheromone_tao_matrix[indexStartPoint][indexEndPoint]
            * Math.pow(this.getEtaValue(startPoint, indexEndPoint), this.beta)
            * this.getHumanProbabilisticBaseKpi('1', endPoint);
    }

    getBestNextNode(startPoint, reachablePoint) {
        if (!reachablePoint.length) {
            return 'finish';
        }

        const point = {};
        const randomNumber = Math.random();

        const equationValues = reachablePoint.reduce((acc, item) => {
            acc[item] = this.equationValue(startPoint, item);
            return acc;
        }, {});

        if (FINISH_POINT_VALUE in equationValues && Object.keys(equationValues).length !== 1) {
            delete equationValues[FINISH_POINT_VALUE];
        }

        if (FINISH_POINT_VALUE in equationValues && Object.keys(equationValues).length === 1) {
            return FINISH_POINT_VALUE;
        } else {
            if (randomNumber <= this.ro) {
                for (const [key, value] of Object.entries(equationValues)) {
                    point[key] = 1 - value;
                }
            } else {
                const totalEquationValue = Object.values(equationValues).reduce((sum, value) => sum + value, 0);
                for (const [key, value] of Object.entries(equationValues)) {
                    point[key] = 1 - value / totalEquationValue;
                }
            }

            return Object.keys(point).reduce((maxKey, key) => (point[key] > point[maxKey] ? key : maxKey), -1);
        }
    }

    calculateLen(path) {
        let totalLength = 0;

        for (let index = 0; index < path.length; index++) {
            const value = path[index];
            if (value !== FINISH_POINT_VALUE) {
                totalLength += this.weight_matrix[value][getIndexByKpiIdInFile({ kpi_id: path[index + 1] })];
            }
        }

        return totalLength;
    }

    getRhoValue(humanId, endPointIndex) {
        const endPointEnvScore = this.kpi_env_score.find(item => String(item.kpi_id) === getKeyByIndex(this.weight_matrix, endPointIndex)).score || 0;
        const humanScore = this.human_ability_score.find(item => String(item.id) === humanId).ability_score || 0;

        return (1 - endPointEnvScore) * (1 - humanScore);
    }

    updatePheromone(indexRow, indexColumn, isGlobal = false) {
        if (this.pheromone_tao_matrix[indexRow][indexColumn] !== 0) {
            const currentRhoValue = this.getRhoValue('1', indexColumn);
            const currentPheromoneValue = this.pheromone_tao_matrix[indexRow][indexColumn];

            let updateValue = 0;

            if (isGlobal) {
                updateValue = (1 - currentRhoValue) * currentPheromoneValue + currentRhoValue * (1 / this.best_path_length);
            } else {
                updateValue = this.default_pheromone_tao_matrix[indexColumn][indexRow] * currentRhoValue +
                    (1 - currentRhoValue) * currentPheromoneValue;
            }

            this.pheromone_tao_matrix[indexRow][indexColumn] = updateValue;
        }
    }

    updateLocalPheromone() {
        for (let indexRow = 0; indexRow < this.pheromone_tao_matrix.length; indexRow++) {
            for (let indexColumn = 0; indexColumn < this.pheromone_tao_matrix[indexRow].length; indexColumn++) {
                this.updatePheromone(indexRow, indexColumn);
            }
        }
    }

    updateGlobalPheromone() {
        for (let index = 0; index < this.best_path.length; index++) {
            const item = this.best_path[index];
            if (item !== FINISH_POINT_VALUE) {
                const indexItem = getIndexByKpiIdInFile({ kpi_id: item });
                const indexNextItem = getIndexByKpiIdInFile({ kpi_id: this.best_path[index + 1] });
                this.updatePheromone(indexItem, indexNextItem, true);
            }
        }
    }

    run() {
        for (let generationCount = 0; generationCount < this.generation; generationCount++) {
            const currentGenPath = {};

            for (let populationCount = 0; populationCount < this.population; populationCount++) {
                const currentAntPath = [START_POINT_VALUE];

                while (currentAntPath.length !== this.list_kpi_unit.length) {
                    const reachablePoint = this.getListAvailableNextPoint(currentAntPath[currentAntPath.length - 1], currentAntPath);
                    const bestNextPoint = this.getBestNextNode(currentAntPath[currentAntPath.length - 1], reachablePoint);
                    currentAntPath.push(bestNextPoint);
                }

                const currentAntLength = this.calculateLen(currentAntPath);
                currentGenPath[currentAntLength] = currentAntPath;
            }

            this.updateLocalPheromone();

            this.best_path_length = Math.max(...Object.keys(currentGenPath));
            this.best_path = currentGenPath[this.best_path_length];

            this.updateGlobalPheromone();
        }

        console.log(this.best_path, this.best_path_length);
    }
}

const aco = new AntSystemOptimization(10, 10);
aco.run();
