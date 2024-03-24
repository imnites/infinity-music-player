import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { AiFillPlayCircle, AiFillPauseCircle } from 'react-icons/ai';
import { BiSkipNext, BiSkipPrevious } from 'react-icons/bi';
import { IconContext } from 'react-icons';
import PropTypes from 'prop-types';
import { Howl } from 'howler';

const isNullOrUndefined = (val) => val === null || val === undefined;

export const Player = ({ songQueue, aiMode, removeFromQueue }) => {
  const [id, setId] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [seconds, setSeconds] = useState(0);
  const [currTime, setCurrTime] = useState({
    min: 0,
    sec: 0
  });
  const [autoPlay, setAutoplay] = useState(false);
  const [current, setCurrent] = useState(0);

  const sounds = useMemo(
    () =>
      songQueue && songQueue.length > 0
        ? songQueue.map(
            (songPath) =>
              new Howl({
                src: require('../assets/mp3-songs/' + songPath),
                onplay: () => {
                  setIsPlaying(true);
                },
                onpause: () => {
                  setIsPlaying(false);
                },
                onstop: () => {
                  setIsPlaying(false);
                  setCurrTime({ min: 0, sec: 0 });
                },
                onend: () => {
                  setIsPlaying(false);
                  setAutoplay(true);
                  setCurrent(current + 1 < songQueue.length ? current + 1 : 0);
                  if (aiMode) {
                    removeFromQueue();
                  }
                }
              })
          )
        : null,
    [aiMode, current, removeFromQueue, songQueue]
  );

  const time = useMemo(() => {
    const getDuration = () => {
      try {
        const _duration = sounds[current].duration(id);

        const sec = Math.floor(_duration % 60);
        const min = Math.floor(_duration / 60);

        return {
          min,
          sec,
          duration: Math.floor(_duration)
        };
      } catch (ex) {
        return null;
      }
    };

    return getDuration();
  }, [id, sounds, current]);

  const onPlayClick = useCallback(() => {
    if (sounds[current]) {
      const _id = sounds[current].play();
      setId(_id);
    }
  }, [sounds, current]);

  const onPauseClick = useCallback(() => {
    if (sounds[current]) {
      sounds[current].pause();
    }
  }, [sounds, current]);

  useEffect(() => {
    const interval = setInterval(() => {
      if (sounds && sounds[current]) {
        setSeconds(sounds[current].seek());
        const min = Math.floor(sounds[current].seek() / 60);
        const sec = Math.floor(sounds[current].seek() % 60);

        setCurrTime({
          min,
          sec
        });
      }
    }, 1000);
    return () => clearInterval(interval);
  }, [sounds, current]);

  const onPrevClick = useCallback(() => {
    sounds[current].stop();
    if (current - 1 >= 0) {
      sounds[current - 1].play();
      setCurrent(current - 1);
    } else {
      sounds[songQueue.length - 1].play();
      setCurrent(songQueue.length - 1);
    }
  }, [sounds, current, songQueue.length]);

  const onNextClick = useCallback(() => {
    sounds[current].stop();
    if (current + 1 < songQueue.length) {
      sounds[current + 1].play();
      setCurrent(current + 1);
    } else {
      sounds[0].play();
      setCurrent(0);
    }
  }, [sounds, current, songQueue.length]);

  useEffect(() => {
    if (sounds && sounds[current] && (autoPlay || aiMode)) {
      const _id = sounds[current].play();
      setId(_id);
    }
  }, [autoPlay, sounds, current, aiMode]);

  return (
    <div className="component">
      <h2>Playing Now</h2>
      <img className="musicCover" src="https://picsum.photos/200/200" alt="Not Available" />
      <div>
        <h3 className="title">
          {songQueue[current] ? songQueue[current].split('/')[1] : 'No song to play'}
        </h3>
        <p className="subTitle">
          {songQueue[current] ? songQueue[current].split('/')[0] : 'No Subtitle'}
        </p>
      </div>
      <div>
        <button
          disabled={isNullOrUndefined(sounds && sounds.length)}
          className="playButton"
          onClick={onPrevClick}>
          <IconContext.Provider value={{ size: '3em', color: '#27AE60' }}>
            <BiSkipPrevious />
          </IconContext.Provider>
        </button>
        {!isPlaying ? (
          <button
            disabled={isNullOrUndefined(sounds && sounds.length)}
            className="playButton"
            onClick={onPlayClick}>
            <IconContext.Provider value={{ size: '3em', color: '#27AE60' }}>
              <AiFillPlayCircle />
            </IconContext.Provider>
          </button>
        ) : (
          <button
            disabled={isNullOrUndefined(sounds && sounds.length)}
            className="playButton"
            onClick={onPauseClick}>
            <IconContext.Provider value={{ size: '3em', color: '#27AE60' }}>
              <AiFillPauseCircle />
            </IconContext.Provider>
          </button>
        )}
        <button
          disabled={isNullOrUndefined(sounds && sounds.length)}
          className="playButton"
          onClick={onNextClick}>
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
            onChange={(e) => {
              sounds[current].seek(e.target.value);
            }}
          />
        ) : null}
      </div>
    </div>
  );
};

Player.propTypes = {
  songQueue: PropTypes.array,
  aiMode: PropTypes.bool,
  removeFromQueue: PropTypes.func
};
