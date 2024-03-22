import React, { useCallback, useState } from 'react';
import { Player } from './Music';
import { CustomWebcam } from './Webcam';
import { Box, Stack, Typography } from '@mui/material';
import { AntSwitch } from './Components';

export const Home = () => {
  const [aiMode, setAIMode] = useState(false);
  const onChange = useCallback((e) => {
    setAIMode(e && e.target && e.target.checked);
  }, []);

  return (
    <>
      <Box sx={{ display: 'flex' }}>
        <Box sx={{ padding: '16px', margin: 'auto' }}>
          <Player />
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
          <CustomWebcam />
        </Box>
      ) : null}
    </>
  );
};
