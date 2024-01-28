import {readFileSync, writeFileSync} from 'fs'

const inputFilePath = 'data.json';
const inputData = readFileSync(inputFilePath, 'utf-8');
const jsonData = JSON.parse(inputData);

const extractedData = jsonData.countries.country.map(country => ({
  countryCode: country.countryCode,
  countryName: country.countryName,
  currencyCode: country.currencyCode,
}));

const outputFilePath = 'output.json'; // Update with your desired output file path
writeFileSync(outputFilePath, JSON.stringify(extractedData, null, 2));
