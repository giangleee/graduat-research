import {DataFrame} from 'dataframe-js'
import { readFileSync } from 'fs';

export class Human {
    constructor(id, name, abilityScore) {
        this.id = parseInt(id);
        this.name = name;
        this.ability_score = parseFloat(abilityScore);
    }
}

export const getListHuman = (filename = 'HumanAbilityScore.csv') => {
    const csvData = readFileSync(filename, 'utf8');

    const csvArray = csvData
        .trim()
        .split('\n')
        .map(line => line.split(','))
        .map(cols => ({
            human_id: cols[0],
            name: cols[1],
            abilityScore: cols[2],
    }));
    csvArray.shift()
    const listHuman = csvArray.map(row => new Human(row.human_id, row.name, row.abilityScore));
    return listHuman
}

