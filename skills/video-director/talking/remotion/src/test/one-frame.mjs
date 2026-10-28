// node src/test/one-frame.mjs <props.json> <frame> <out.png>  -> renders one still PNG
import {execFileSync} from 'node:child_process';
import {readFileSync} from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const [props, frame, out] = process.argv.slice(2);
execFileSync(process.execPath, [path.join(path.dirname(fileURLToPath(import.meta.url)), '..', '..', 'node_modules', '@remotion', 'cli', 'remotion-cli.js'), 'still', 'Reel', out, '--props', props, '--frame', frame, '--image-format', 'png'],
  {stdio: 'inherit'});
const png = readFileSync(out);
console.log('wrote', out, png.length, 'bytes');
