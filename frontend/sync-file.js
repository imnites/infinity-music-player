/* eslint-disable no-undef */
const fs = require('fs');
const path = require('path');

const readFiles = (songsPath) => fs.readdirSync(path.resolve(__dirname, songsPath));

const labelAndFiles = {};

labelAndFiles.happy = readFiles('./src/assets/mp3-songs/happy');
labelAndFiles.sadness = readFiles('./src/assets/mp3-songs/sadness');

fs.writeFile('./src/mp3s.json', JSON.stringify(labelAndFiles), 'utf8', () => {
  console.log('successfully added');
});
