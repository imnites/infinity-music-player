/* eslint-disable no-undef */
const fs = require('fs');
const path = require('path');

const audioExtensions = new Set([
  '.mp3',
  '.mpeg',
  '.opus',
  '.ogg',
  '.oga',
  '.wav',
  '.aac',
  '.caf',
  '.m4a',
  '.m4b',
  '.mp4',
  '.weba',
  '.webm',
  '.dolby',
  '.flac'
]);

const readFiles = (songsPath) => {
  if (fs.existsSync(songsPath)) {
    const res = [];
    const items = fs.readdirSync(path.resolve(__dirname, songsPath));

    for (const item of items) {
      if (audioExtensions.has(path.extname(item))) {
        res.push(item);
      }
    }

    return res;
  }

  fs.mkdirSync(songsPath, { recursive: true });
  return [];
};

const labelAndFiles = {};

labelAndFiles.happy = readFiles('./src/assets/mp3-songs/happy');
labelAndFiles.sadness = readFiles('./src/assets/mp3-songs/sadness');
labelAndFiles.anger = readFiles('./src/assets/mp3-songs/anger');
labelAndFiles.contempt = readFiles('./src/assets/mp3-songs/contempt');
labelAndFiles.disgust = readFiles('./src/assets/mp3-songs/disgust');
labelAndFiles.fear = readFiles('./src/assets/mp3-songs/fear');
labelAndFiles.surprise = readFiles('./src/assets/mp3-songs/surprise');

fs.writeFile('./src/mp3s.json', JSON.stringify(labelAndFiles), 'utf8', () => {
  console.log('successfully synced');
});
