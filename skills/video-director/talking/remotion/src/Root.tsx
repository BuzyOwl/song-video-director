import {Composition} from 'remotion';
import {Reel} from './Reel';
import type {ReelProps} from './types';

const defaults: ReelProps = {src: 'job/cut.mp4', fps: 30, w: 1080, h: 1920, dur: 2, srcDur: 2, cuts: [], face: [[0.5, 0.4, 0.4, 0.22]],
  punch: 1.12, zoom: [], chunks: [], cards: [], sfx: [], accent: '#FFD23F', font: 'Montserrat-ExtraBold', lang: 'en', capSize: 78};

export const Root = () => (
  <Composition id="Reel" component={Reel} fps={30} width={1080} height={1920} durationInFrames={60}
    defaultProps={defaults}
    calculateMetadata={({props}) => ({fps: props.fps, width: props.w, height: props.h,
      durationInFrames: Math.round(props.dur * props.fps)})} />
);
