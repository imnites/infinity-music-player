import React, { useCallback, useState } from 'react';
import { Player } from './Music';
import { CustomWebcam } from './Webcam';
import { Box, Stack, Typography } from '@mui/material';
import { AntSwitch } from './Components';
import mp3s from './mp3s.json';

const allSongs = () => {
  const songs = [];
  for (const key in mp3s) {
    for (const song of mp3s[key]) {
      songs.push(`${key}/${song}`);
    }
  }
  return songs;
};

export const Home = () => {
  const [aiMode, setAIMode] = useState(false);
  const [songQueue, setSongQueue] = useState(allSongs());

  const onChange = useCallback((e) => {
    if (e && e.target && e.target.checked) {
      setAIMode(true);
      setSongQueue([]);
    } else {
      setAIMode(false);
      setSongQueue(allSongs());
    }
  }, []);

  const addSongToQueue = useCallback(
    (songPath) => {
      if (songQueue.length === 0) {
        setSongQueue([songPath]);
      }
    },
    [songQueue]
  );

  const removeFromQueue = useCallback(() => {
    setSongQueue([]);
  }, []);

  return (
    <>
      <Box sx={{ display: 'flex' }}>
        <Box sx={{ padding: '16px', margin: 'auto' }}>
          <Player songQueue={songQueue} aiMode={aiMode} removeFromQueue={removeFromQueue} />
        </Box>
      </Box>
      <Box sx={{ display: 'flex' }}>
        <Box sx={{ padding: '16px', margin: 'auto' }}>
          <Stack
            sx={{ marginLeft: 'auto', marginRight: 'auto', marginTop: '32px' }}
            direction="row"
            spacing={1}
            alignItems="center">
            <Typography>{`Switch to ${aiMode ? 'normal' : 'AI'} Mode`}</Typography>
            <AntSwitch
              checked={aiMode}
              onChange={onChange}
              inputProps={{ 'aria-label': 'ant design' }}
            />
          </Stack>
        </Box>
      </Box>
      {aiMode ? (
        <Box sx={{ position: 'absolute', right: 0, top: 0, padding: '32px' }}>
          <CustomWebcam addSongToQueue={addSongToQueue} />
        </Box>
      ) : null}
    </>
  );
};
