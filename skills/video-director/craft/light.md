# Craft: look and light (materials, lighting, colour)

Load when building a set, materials or lighting, or when a draft reads cheap CG: too bright, too smooth, everything
glowing, floating in black, "game-like". Adapted from Imaginative-Prompting/claude-video-skills `look-and-light` (MIT)
and the user's own film-cinematographer notes. The piece's STYLE.md can overrule any of this on purpose; a flat
graphic look is a choice, not a mistake.

## Light carries emotion
- Time of day per beat: dawn hope · golden hour love, nostalgia · blue hour reflection · night warm pools (lamps, fire).
- **Motivate every light** (sun, window, lamp, fire, phone). Characters get a key, a rim for separation, an eye light in
  close-ups. Flat even lighting is the single biggest "game" tell.
- Palette arc across the film (cool start warming to the climax, or warm memory vs cooler present); 2–3 hues a scene.
- Haze and depth fog give scale and memory feel.

## 3D procedure (three.js, Blender, similar)
1. **Real textures on every surface:** PBR albedo + roughness + normal (Poly Haven CC0). Texel density that holds at the
   closest framing. Log each in CREDITS.md. Smooth flat-shaded surfaces read as placeholders.
2. **Keep it dark.** Sets and crowds muted, lit only by real sources at real reach; only what should read is lit.
3. **Only real light sources glow** (bulbs, screens, LED strips, lit windows, fire). Every other surface: emissive 0.
   An authored emissive under ~0.4 usually means a surface faking its own light.
4. **Real falloff (three.js):** point/spot `decay = 2` plus a `distance`; set intensity at the nearest subject
   (illuminance = intensity / d²). `RectAreaLight` has no range and casts no shadow, so a small practical (phone, bulb) is
   a short-range Spot/PointLight gone within ~1 m. No camera-side fill; no emissive rim terms lighting people evenly.
5. **A dark space, not a void:** a floor, haze or dim structure lit by the scene's own sources, falling off fast.
6. **Judge colour in the film's light:** tune on a still of the real scene and sample the rendered pixel (a grey tuned in
   a lineup came out charcoal in the shot).
7. **Stylised form, real colours:** take colours and markings from photos; build a clean stylised form. Never fit a sculpt
   to photos (a pose's squashed cheek becomes permanent).
8. **A style needs structure, not a filter:** a comic look worked through ink outlines, screen-fixed halftone, hard light
   bands, saturated world vs muted hero, one accent colour reserved for one character.
9. Separation: one focal value per shot, warm vs cool, a palette per place, colourblind-safe.

## Failure modes
- Naming the cause from a list of lights. Solo each light and measure what it adds to the subject.
- An audit whose masks leak (unoverridable materials draw as themselves). Look at the leaked pixels before reporting.
- A bloom veil from a big white surface (an LED wall) washing everything.

## Verify
List every emissive material and every light (intensity, distance, decay) before a lighting pass; zero the fakes at
source. Stills for anything lit for no reason; zoom dark areas for banding; textures at full res at their closest framing.
