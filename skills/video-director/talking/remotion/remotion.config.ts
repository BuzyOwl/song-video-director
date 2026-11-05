import {Config} from '@remotion/cli/config';
import os from 'node:os';
import fs from 'node:fs';
// Heavy temp on the big drive: Chrome profiles and bundles otherwise fill C: (14 GB free).
process.env.TEMP = process.env.TMP = 'D:\\03_Projects\\tmp';
fs.mkdirSync(process.env.TEMP, {recursive: true});
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(90);
Config.setConcurrency(Math.max(2, Math.min(4, os.cpus().length)));
Config.setChromiumOpenGlRenderer('angle');
Config.setOverwriteOutput(true);
