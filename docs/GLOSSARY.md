# Technical words cheat sheet

Say these without fumbling.

## Glossary

| Group | Term | Say it like this | Example in our films |
|---|---|---|---|
| Frame | Frame | One still image. 30 per second. | Every frame is a pure function of time. |
| Frame | FPS | Frames per second: how smooth motion feels. | Film 30 fps; line-boil effect at 12 fps. |
| Frame | Resolution | Pixels wide x tall. | 1080p landscape, 1080x1920 for Shorts. |
| Frame | Aspect ratio | Width : height shape. | 16:9 film, 9:16 vertical Short. |
| Frame | Safe area | Zone where text is never cut off by the phone UI. | Lyrics kept inside it. |
| Composition | Framing | What is inside the rectangle and where. | Tiny figure in a wide = weak framing. |
| Composition | Shot types | Wide / medium / close-up / extreme close-up. | Close-up for the emotional line. |
| Composition | Rule of thirds | Put the subject on a third line, not the centre. |  |
| Composition | Negative space | Empty area that gives the subject room. | Lyric text sits there. |
| Composition | Scrim | Soft dark/light gradient behind text for contrast. | Lyric readability on busy plates. |
| Composition | Hook | The first 1.5 s that stops the scroll. | Every plan needs one. |
| Camera | Pan / tilt | Camera turns left-right / up-down. |  |
| Camera | Dolly | Camera physically moves toward/away. | 2.5D dolly on still plates. |
| Camera | Crane | Camera moves up/down through space. |  |
| Camera | Rack focus | Focus shifts from near to far subject. | Close-up lens pass in Toota Naksha. |
| Camera | Depth of field (DoF) | Blur outside the focus plane. | GPU bokeh particles. |
| Camera | Parallax | Near layers move more than far layers. | Fake depth from flat plates. |
| Camera | 2.5D | Flat images placed in 3D space and moved by a 3D camera. | Toota Naksha floor-plane projection. |
| Layers | Layer | A separate stack level: background, mid, character, text. |  |
| Layers | Plate | A background image/art layer of the scene. | Calibrated horizon + vanishing points. |
| Layers | Alpha / transparency | The see-through part of an image. | Sprites keyed to transparent PNG. |
| Layers | Compositing | Stacking layers into one final image. | Canvas2D compositor. |
| Layers | Blend mode | How a layer mixes with the one below. | Screen for glow, multiply for shadow. |
| Layers | Mask / matte | A shape that hides or reveals part of a layer. | Line-wipe transition. |
| Animation | Sprite | A flat character image or one pose of it. | Pose table, swim atlases. |
| Animation | Sprite sheet / atlas | Many poses packed into one image. | Goldfish swim atlas. |
| Animation | Cut-out animation | Flat parts moved/rotated like paper puppets. | Basement Goldfish. |
| Animation | Keyframe | A saved value at a time (position at 2.0 s). |  |
| Animation | Tweening / interpolation | Computer fills frames between keyframes. |  |
| Animation | Easing | Acceleration curve of a move (ease-in/out). | Settle on the beat. |
| Animation | Forward kinematics (FK) | Pose a body by setting joint angles root-to-tip. | Mannequin in Jod Ke Dekh. |
| Animation | Rig | Skeleton + controls that pose a model. | Blender hand. |
| Animation | Line boil | Outlines wobble frame to frame, hand-drawn feel. | 12 fps wobble in p5. |
| Animation | Crossfade ghost | Blending two body poses makes a double image. | Never crossfade bodies. |
| Animation | Motion blur | Smear of moving objects, like a real shutter. | Subframe renders averaged. |
| 3D / CGI | CGI | Anything made/rendered by computer graphics. | three.js scenes, Blender props. |
| 3D / CGI | Mesh | A 3D surface made of triangles. | GLB hand. |
| 3D / CGI | Texture | Image wrapped onto a mesh. | Lyrics drawn onto a TextPlane. |
| 3D / CGI | Shader | Small GPU program that decides pixel/vertex looks. | Paper, halftone, finish shader. |
| 3D / CGI | Render pass | One stage of the image pipeline. | ScenePass, Bloom, Output. |
| 3D / CGI | Bloom / halation | Bright areas glow into surroundings. | Post finish. |
| 3D / CGI | Vignette / grain | Darkened edges / film noise. | Finish shader. |
| 3D / CGI | Chromatic aberration | Colour fringes at the edges, lens flaw. | Cinematic edge. |
| 3D / CGI | Particles | Many tiny moving points (dust, sparks). | GPU bokeh dust. |
| Code | Deterministic | Same time in = same image out. No randomness/state. | Lets you render any frame alone. |
| Code | Pure function of time | frame = f(t) only. | renderFilm(ctx, t) |
| Code | Canvas (HTML Canvas / Canvas2D) | Browser surface you draw pixels onto with code. | p5.js and the TN compositor. |
| Code | WebGL / GPU | Browser 3D drawing on the graphics card. | three.js, shaders. |
| Code | Motion Canvas | TypeScript library: write 2D animation as generator code with a live timeline editor. | Alternative to Remotion for vector/diagram work. |
| Code | Remotion | React framework that renders video frame by frame to MP4. | Host for TN and JKD. |
| Code | p5.js | Friendly creative-coding library on Canvas. | Basement Goldfish. |
| Code | three.js | JavaScript 3D engine on WebGL. | Jod Ke Dekh. |
| Code | Headless | Runs without a visible window. | Blender -b, puppeteer. |
| Code | Concurrency | Frames rendered in parallel. | --concurrency=4 |
| Code | Encode / mux | Compress to MP4 / join audio and video. | ffmpeg, CRF 17. |
| Audio | BPM | Beats per minute: sets the motion language. | 63 BPM breathes; 130 BPM cuts. |
| Audio | Beat grid | Evenly spaced beat times across the song. | Drift-free grid. |
| Audio | Onset | The moment a sound starts. | Per-frame onset. |
| Audio | Energy curve | Loudness over time; find section hits. | Mark chorus drops. |
| Audio | Forced alignment | Matching known lyrics to exact audio times. | Whisper / MMS aligner. |
| Audio | Whisper | Speech-to-text model that gives word times. | faster-whisper large-v3. |
| Audio | Stem | One isolated track (vocals only). | Align on the vocal stem. |
| Type | Kinetic typography | Words that move/animate with the audio. | Lyric video. |
| Type | Lane | A fixed screen zone for one type of text. | Main / echo / adlib lanes. |
| Type | Lyric tag M / A2 / A1 / E | Main, adlib-2, adlib-1, echo. | Per-word tagging. |
| Post | Colour grade | Overall colour mood. |  |
| Post | Contact sheet | Grid of frames to review a whole piece at a glance. | tools/sheet.mjs |
| Post | Thumbnail | The still that sells the click. | Taken from a film frame. |
| Style | Signature moment | The one shot people remember. | Hand signing the lyric sheet. |
| Style | Callback | Later scene echoes an earlier image. | Ending echoes opening. |
