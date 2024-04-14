import { useCallback, useState, useMemo, useEffect } from 'react';
import mp3s from './mp3s.json';
import { Howl } from 'howler';

const allSongs = () => {
  const songs = [];
  for (const key in mp3s) {
    for (const song of mp3s[key]) {
      songs.push(`${key}/${song}`);
    }
  }

  return songs;
};

const mapToHowls = ({ songs, onplay, onpause, onstop, onend }) =>
  songs.map(
    (songPath) =>
      new Howl({
        src: require('./assets/mp3-songs/' + songPath),
        onplay,
        onpause,
        onstop,
        onend
      })
  );

export const usePlayer = () => {
  const [aiMode, setAIMode] = useState(false);

  const [id, setId] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [seconds, setSeconds] = useState(0);
  const [currTime, setCurrTime] = useState({
    min: 0,
    sec: 0
  });
  const [current, setCurrent] = useState(0);

  const onplay = useCallback(() => {
    setIsPlaying(true);
  }, []);

  const onpause = useCallback(() => {
    setIsPlaying(false);
  }, []);

  const onstop = useCallback(() => {
    setIsPlaying(false);
    setCurrTime({ min: 0, sec: 0 });
  }, []);

  const onend = useCallback(() => {
    setIsPlaying(false);
  }, []);

  const [sounds, setSounds] = useState(
    mapToHowls({
      songs: allSongs(),
      onplay,
      onpause,
      onstop,
      onend
    })
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
  }, [current, sounds]);

  const onPauseClick = useCallback(() => {
    sounds[current] && sounds[current].pause();
  }, [current, sounds]);

  const onPrevClick = useCallback(() => {
    sounds[current] && sounds[current].stop();

    if (current - 1 >= 0) {
      sounds[current - 1] && sounds[current - 1].play();
      setCurrent(current - 1);
    } else {
      sounds[sounds.length - 1] && sounds[sounds.length - 1].play();
      setCurrent(sounds.length - 1);
    }
  }, [current, sounds]);

  const onNextClick = useCallback(() => {
    sounds[current].stop();
    if (current + 1 < sounds.length) {
      sounds[current + 1].play();
      setCurrent(current + 1);
    } else {
      sounds[0].play();
      setCurrent(0);
    }
  }, [current, sounds]);

  const onAIModeSwitchChange = useCallback(
    (e) => {
      sounds.forEach((sound) => {
        sound.unload();
      });

      if (e && e.target && e.target.checked) {
        setAIMode(true);
        setSounds([]);
      } else {
        setAIMode(false);
        setSounds(
          mapToHowls({
            songs: allSongs(),
            onplay,
            onpause,
            onstop,
            onend
          })
        );
      }
    },
    [onend, onpause, onplay, onstop, sounds]
  );

  const changeSong = useCallback(
    (songName) => {
      if (songName && sounds?.length === 0) {
        const s = mapToHowls({
          songs: [songName],
          onplay,
          onpause,
          onstop,
          onend: () => {
            setSounds([]);
            setIsPlaying(false);
            setAIMode(false);
            setAIMode(true);
          }
        });

        const _id = s[0].play();
        setId(_id);
        setSounds(s);
      }
    },
    [onpause, onplay, onstop, sounds?.length]
  );

  const onSeek = useCallback(
    (e) => {
      sounds[current].seek(e.target.value);
      setSeconds(e.target.value);
    },
    [current, sounds]
  );

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

  return {
    currentSongName: 'Song 1',
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
    seconds,
    time
  };
};
