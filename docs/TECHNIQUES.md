# Techniques: traditional vs code, and how to combine them

## Techniques

| Technique | What it is (1 line) | Traditional version | Strength | Limit | Tools | Use in our code pipeline |
|---|---|---|---|---|---|---|
| Sprites | Flat character images/poses swapped or moved | Cel animation / cut-out puppets | Cheap, charming, easy to swap characters | No true 3D turn, pose limit, soft when upscaled | p5.js, PIL/OpenCV keying, Remotion | Basement Goldfish pose table; never crossfade bodies |
| CGI | Computer-generated 3D worlds, lit and rendered | Pixar / VFX pipeline in Maya, Blender | Real camera, light, depth; no art drift | Slow render, needs modelling skill | three.js, Blender, Remotion | Jod Ke Dekh: mannequin + 3D set, Blender hand |
| Layers | Separate stack levels composited into one image | Photoshop / After Effects layer stack, multiplane camera | Control, reuse, parallax | Layer seams; edges can halo | Canvas2D, WebGL compositor | Backgrounds, plates, characters, type, FX each own a layer |
| Framing | Choice of what is in shot and how big | Cinematography / storyboard shot list | Directs attention and emotion | Bad framing cannot be fixed by effects | Camera code, 2.5D projection | Wide vs close per lyric; never type over a face |
| Canvas | Browser pixel surface you draw on with code (Canvas2D) | Painting on a physical canvas | Simple, fast, universal | CPU-bound for heavy effects | p5.js, Canvas2D API | Compositor for plates and sprites |
| Motion Canvas | TS library, animation as generator code + live editor | After Effects timeline, but typed | Great for vector, diagrams, explainer feel | 2D focused; smaller ecosystem than Remotion | motioncanvas.io | Option for explainer/diagram sections or clean motion graphics |
| Code-based animation | Every frame computed from time by code | Hand keyframing in a GUI | Repeatable, exact beat sync, agent-friendly, version-controlled | No hands-on art direction feel; setup cost | Remotion, p5, three.js, ffmpeg | The core of this skill: pure function of time |
| Keyframe / tween | Set values at times, computer interpolates | Flash / After Effects keyframes | Fast, familiar | Looks mechanical without easing | GSAP, Remotion interpolate | Easing tied to beat grid |
| Shaders | GPU programs that style every pixel | Optical filters, lab processing | Unique looks: paper, halftone, glow | Hard to debug; GL state quirks | GLSL, three.js, WebGL2 | Paper slabs, halftone, finish pass |
| Procedural generation | Invent visuals from rules/noise, no art asset | Generative art, particle sims | Infinite variety; no source art needed | Can feel random without direction | Noise, particles, shaders | Invent when you cannot generate new art |
| 2.5D / parallax | Flat plates in 3D space with a moving camera | Multiplane camera, Ken Burns | Depth from stills | Edges stretch past small angles | Homography, floor-plane depth | Toota Naksha camera moves |
| Kinetic typography | Text animated to the audio | Title design, lyric cards | Reads as story if lyrics live in the world | Phone legibility traps | Canvas textures, TextPlane | Lyrics inside phone chat, whiteboard, invoice |
| Motion graphics | Designed shapes/graphics animated | After Effects work | Clean, modern, explainer | Can look generic | Motion Canvas, Remotion, Lottie | Wow beats at section hits |
| Rotoscoping / tracking | Follow real footage with art or masks | Frame-by-frame trace | Ties art to live footage | Labour heavy | OpenCV, After Effects | Use only for real-footage cutouts |
| Stop-motion look | Low fps stepped motion, handmade feel | Clay / paper stop-motion | Texture and charm | Slow in real life | Step interpolation, 12 fps boil | Line boil, stepped limb swap |
| Live action | Real filmed footage | Camera shoot | Real human emotion | Needs shoot and crew | Camera + Python/Remotion cut | See talking-head-director skill |
| AI-generated assets | Images/video/music from models | Illustration, stock, composer | Fast art and music | Identity drift, credit honestly | Suno, image models | Assets are actors; declare AI use |

## Pipeline

| Stage | Traditional way | Code-first way | What to keep from tradition |
|---|---|---|---|
| 1 Idea / script | Treatment, lyric sheet, mood board | Song facts JSON + plan doc | Strong concept, one signature moment |
| 2 Storyboard | Hand-drawn thumbnails, animatic | Scene table with ranges, camera, light, metaphor | Shot list thinking |
| 3 Design | Concept art, character sheets | Generated art + calibrated plates, hard rules | Consistent style bible |
| 4 Layout / camera | Layout artist sets camera | Camera functions, 2.5D / 3D camera | Framing and shot variety |
| 5 Animation | Keyframes by hand in AE / Maya | Pure function of time, beat-grid easing | Timing, easing, anticipation |
| 6 Lighting / FX | Compositor adds glow, particles | Shaders, bloom, particles in the engine | Restraint: stillness lets peaks land |
| 7 Audio sync | Editor cuts to the beat by eye | Measured BPM, onsets, aligned words | Ear-check anyway |
| 8 Render | Render farm | Parallel frame render + ffmpeg mux | Check the final file |
| 9 Review | Dailies / director notes | Contact sheets, strips, crops at timestamps | Look before you say fixed |
| 10 Publish | Delivery + poster | Thumbnail from a film frame, upload pack | Credit honestly |

## Style recipes

| Style name | Traditional ingredient | Code ingredient | Result / when to use | Done in |
|---|---|---|---|---|
| Paper puppet comedy | Cut-out sprites | p5 brush + line boil + beat grid | Handmade, funny, indie tracks | Basement Goldfish |
| Cinematic ballad | Painted plates + dolly + grading | 2.5D camera + WebGL post + audio-reactive finish | Slow emotional songs | Toota Naksha |
| Lyrics inside the world | Set design + props | three.js scene table + TextPlane + Blender prop | Rap/story songs where words are the plot | Jod Ke Dekh |
| Clean explainer lyric video | Motion graphics | Motion Canvas or Remotion + kinetic type | Fast, readable, brand-safe | Next experiment |
| Sprite x CGI hybrid | Cut-out character in a lit 3D set | Sprite planes in three.js + shadows | Flat character, deep world: distinct look | Idea to try |
| Procedural dream | Abstract film / VJ visuals | Shaders + noise + energy curve | Instrumental or when no art exists | Idea to try |
| Live + code overlay | Talking head shoot | Remotion graphics + captions | Reels, explainers | talking-head-director |
