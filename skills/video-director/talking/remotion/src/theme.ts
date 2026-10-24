import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';

// Montserrat and Noto are variable fonts: the declared weight selects the wght instance.
export const FONTS = {
  'Montserrat-ExtraBold': {url: 'fonts/Montserrat-ExtraBold.ttf', weight: '800'},
  'Poppins-Bold': {url: 'fonts/Poppins-Bold.ttf', weight: '700'},
  'NotoSansDevanagari-Bold': {url: 'fonts/NotoSansDevanagari-Bold.ttf', weight: '800'},
} as const;

let loaded: Promise<void> | null = null;
export const ensureFonts = () => {
  if (!loaded) {
    loaded = Promise.all(
      Object.entries(FONTS).map(([family, f]) => loadFont({family, url: staticFile(f.url), weight: f.weight})),
    ).then(() => undefined);
  }
  return loaded;
};
export const fontStack = (font: string) => `'${font}', 'NotoSansDevanagari-Bold', sans-serif`;
export const SHADOW = '0 2px 0 rgba(0,0,0,.85), 0 10px 28px rgba(0,0,0,.45)';
export const SCRIM = 'linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,.35) 100%)';
