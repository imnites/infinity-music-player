import React, { useRef, useEffect } from 'react';
import Webcam from 'react-webcam';
import PropTypes from 'prop-types';
import mp3s from '../mp3s.json';

const serverBaseURL = 'http://localhost:8080/';

const getEmotionOfImage = async (base64) =>
  fetch(serverBaseURL, {
    Method: 'POST',
    Headers: {
      Accept: '*/*',
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    },
    Body: {
      base64
    },
    Cache: 'default'
  })
    .then(() => {
      return { label: 'sadness', percentage: 90 };
    })
    .catch(() => {
      return { label: 'sadness', percentage: 92 };
    });

const getSongName = (label) => {
  const items = mp3s[label] || [];

  if (items.length > 0) {
    return items[Math.floor(Math.random() * items.length)];
  }
};

export const CustomWebcam = ({ addSongToQueue }) => {
  const webcamRef = useRef(null);

  useEffect(() => {
    const interval = setInterval(async () => {
      if (webcamRef && webcamRef.current) {
        const imageSrc = webcamRef.current.getScreenshot();
        const data = await getEmotionOfImage(imageSrc);
        if (data && data.label && data.percentage > 75 && addSongToQueue) {
          const songName = getSongName(data.label);
          if (songName) {
            addSongToQueue(`${data.label}/${songName}`);
          }
        }
      }
    }, 3000);
    return () => clearInterval(interval);
  }, [addSongToQueue]);

  return (
    <div className="container">
      <Webcam mirrored height={200} width={200} ref={webcamRef} />
    </div>
  );
};

CustomWebcam.propTypes = {
  addSongToQueue: PropTypes.func
};

export default CustomWebcam;
