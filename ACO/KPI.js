// import { parse } from 'csv-parse';
import pkg from 'papaparse';
const { parse } = pkg;
import { DataFrame } from 'dataframe-js'
import { readFileSync } from 'fs';

class KPIUnit {
    constructor(id, name) {
        this.id = id;
        this.name = name;
    }
}

class KPIEnvScore {
    constructor(kpiId, score) {
        this.kpi_id = parseInt(kpiId);
        this.score = score;
    }
}

class KPIHumanScore {
    constructor(kpiId, score, humanId) {
        this.kpi_id = parseInt(kpiId);
        this.score = score;
        this.human_id = parseInt(humanId);
    }
}

export const getKpiWeightMatrix = (filename = 'KpiWeight.csv') => {
    // const csvData = readFileSync(filename, 'utf8');

    // const csvArray = csvData
    //     .trim()
    //     .split('\n')
    //     .map(line => line.split(','))
    // console.log(csvArray[0][1])

    // // Parse CSV content into an array of objects
    // const csvArray = parse(csvData, { columns: true, skip_empty_lines: true });

    // // Create a DataFrame from the array of objects
    // const df = new DataFrame(csvArray);
    // console.log(df)

    // const kpiUnitList = df.map(row => new KPIUnit(row.kpi_id, row.name)).toArray();

    // kpiUnitList.push(new KPIUnit('start', 'Start kpi'));
    // kpiUnitList.push(new KPIUnit('finish', 'Finish kpi'));

    // return kpiUnitList;
    const data = {
        'start': [0.0, 0.426, 0.791, 0.125, 0.893, 0.642, 0.0],
        '1': [0.0, 0.0, 0.987, 0.234, 0.876, 0.567, 0.753],
        '2': [0.0, 0.654, 0.0, 0.409, 0.731, 0.112, 0.923],
        '3': [0.0, 0.312, 0.745, 0.0, 0.567, 0.234, 0.689],
        '4': [0.0, 0.821, 0.453, 0.678, 0.0, 0.789, 0.536],
        '5': [0.0, 0.978, 0.321, 0.567, 0.234, 0.0, 0.428],
        'finish': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    };
    return data
}

export const getListKPIEnvScore = (filename = 'KPIEnvScore.csv') => {
    const csvData = readFileSync(filename, 'utf8');

    const csvArray = csvData
        .trim()
        .split('\n')
        .map(line => line.split(','))
        .map(cols => ({
            kpi_id: cols[0],
            score: cols[1]
    }));
    csvArray.shift()
    const kpiEnvScore = csvArray.map(row => new KPIUnit(row.kpi_id, row.score));
    return kpiEnvScore
}

export const getListKPIUnit = (filename = 'KpiUnit.csv') => {
    const csvData = readFileSync(filename, 'utf8');

    const csvArray = csvData
        .trim()
        .split('\n')
        .map(line => line.split(','))
        .map(cols => ({
            kpi_id: cols[0],
            name: cols[1]
        }));
    csvArray.shift()

    const kpiUnitList = csvArray.map(row => new KPIUnit(row.kpi_id, row.name));

    kpiUnitList.push(new KPIUnit('start', 'Start kpi'));
    kpiUnitList.push(new KPIUnit('finish', 'Finish kpi'));

    return kpiUnitList;
}

export const getListKPIHumanScore = (filename = 'KpiHumanScore.csv') => {
        const csvData = readFileSync(filename, 'utf8');

    const csvArray = csvData
        .trim()
        .split('\n')
        .map(line => line.split(','))
        .map(cols => ({
            human_id: cols[0],
            kpi_id: cols[1],
            score: cols[2],
        }));
    csvArray.shift()
    // console.log(csvArray)
    const kpiUnitList = csvArray.map(row => new KPIHumanScore(row.human_id, row.score, row.kpi_id));
    return kpiUnitList
    // const df = new DataFrame(readFileSync(filename, 'utf8'));
    // return df.toArray().map(row => new KPIHumanScore(row[1].kpi_id, row[1].score, row[1].human_id));
}

export const getIndexByKpiIdInFile = (filename = 'KpiWeight.csv', kpiId = 'start') => {
    const df = new DataFrame(readFileSync(filename, 'utf8'), { index_col: 'kpi_id' });

    let index;
    try {
        index = df.index.getLoc(kpiId);
    } catch (error) {
        index = -1;
    }

    return index;
}

