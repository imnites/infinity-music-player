import React, { useRef, useEffect } from 'react';
import Webcamera from 'react-webcam';
import PropTypes from 'prop-types';
import mp3s from './mp3s.json';

const serverBaseURL = 'http://localhost:8080';

const getEmotionOfImage = async (base64) =>
  fetch(serverBaseURL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      base64
    }),
    Cache: 'default'
  })
    .then((response) => response.json())
    .catch(() => {
      return null;
    });

const getSongName = (label) => {
  const items = mp3s[label] || [];

  if (items.length > 0) {
    return items[Math.floor(Math.random() * items.length)];
  }
};

export const Webcam = ({ changeSong }) => {
  const webcamRef = useRef(null);

  useEffect(() => {
    const interval = setInterval(async () => {
      if (webcamRef && webcamRef.current) {
        const imageSrc = webcamRef.current.getScreenshot();
        const data = await getEmotionOfImage(imageSrc);
        if (data && data.label && changeSong) {
          const songName = getSongName(data.label);

          if (songName) {
            changeSong(`${data.label}/${songName}`);
          }
        }
      }
    }, 3000);
    return () => clearInterval(interval);
  }, [changeSong]);

  return (
    <div className="container">
      <Webcamera mirrored height={200} width={200} ref={webcamRef} />
    </div>
  );
};

Webcam.propTypes = {
  changeSong: PropTypes.func
};

export default Webcam;
