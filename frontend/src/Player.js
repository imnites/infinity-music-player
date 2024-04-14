import React from 'react';
import { Webcam } from './Webcam';
import { Box, Stack, Typography } from '@mui/material';
import { AntSwitch } from './AntSwitch';

import { AiFillPlayCircle, AiFillPauseCircle } from 'react-icons/ai';
import { BiSkipNext, BiSkipPrevious } from 'react-icons/bi';
import { IconContext } from 'react-icons';
import { usePlayer } from './usePlayer';

export const Player = () => {
  const {
    currentSongName,
    aiMode,
    onPrevClick,
    isPlaying,
    onPlayClick,
    onPauseClick,
    onNextClick,
    onAIModeSwitchChange,
    changeSong,
    currTime,
    onSeek,
    time,
    seconds
  } = usePlayer();

  return (
    <>
      <Box sx={{ display: 'flex' }}>
        <Box sx={{ padding: '16px', margin: 'auto' }}>
          <div className="component">
            <h2>Playing Now</h2>
            <img className="musicCover" src="https://picsum.photos/200/200" alt="Not Available" />
            <div>
              <h3 className="title">{currentSongName}</h3>
              <p className="subTitle">No Subtitle</p>
            </div>
            <div>
              <button onClick={onPrevClick}>
                <IconContext.Provider value={{ size: '3em', color: '#27AE60' }}>
                  <BiSkipPrevious />
                </IconContext.Provider>
              </button>
              {!isPlaying ? (
                <button className="playButton" onClick={onPlayClick}>
                  <IconContext.Provider value={{ size: '3em', color: '#27AE60' }}>
                    <AiFillPlayCircle />
                  </IconContext.Provider>
                </button>
              ) : (
                <button className="playButton" onClick={onPauseClick}>
                  <IconContext.Provider value={{ size: '3em', color: '#27AE60' }}>
                    <AiFillPauseCircle />
                  </IconContext.Provider>
                </button>
              )}
              <button className="playButton" onClick={onNextClick}>
                <IconContext.Provider value={{ size: '3em', color: '#27AE60' }}>
                  <BiSkipNext />
                </IconContext.Provider>
              </button>
            </div>
            <div>
              <div className="time">
                {currTime ? (
                  <p>
                    {`${currTime.min} min`} : {`${currTime.sec} sec`}
                  </p>
                ) : null}
                {time ? (
                  <p>
                    {`${time.min} min`} : {`${time.sec} sec`}
                  </p>
                ) : null}
              </div>
              {time ? (
                <input
                  type="range"
                  min="0"
                  max={time.duration}
                  default="0"
                  value={seconds}
                  className="timeline"
                  onChange={onSeek}
                />
              ) : null}
            </div>
          </div>
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
              onChange={onAIModeSwitchChange}
              inputProps={{ 'aria-label': 'ant design' }}
            />
          </Stack>
        </Box>
      </Box>
      {aiMode ? (
        <Box sx={{ position: 'absolute', right: 0, top: 0, padding: '32px' }}>
          <Webcam changeSong={changeSong} />
        </Box>
      ) : null}
    </>
  );
};
