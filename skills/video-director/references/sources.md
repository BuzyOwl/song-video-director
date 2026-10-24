# Sources: free assets, references, MCPs

Read this when the user asks where to get assets or references, or when a scene needs one.
**Last verified: 2026-10-25.** Licenses change, so re-check at download time and log every asset in `CREDITS.md`.

**Defaults:** CC0 with no account (Poly Haven, ambientCG, Kenney).

**License traps:**
- Quaternius is not CC0.
- Coverr and Sonniss forbid AI training.
- Pixabay music carries Content ID claim risk.
- Freesound includes NC sounds.
- Megascans and ShotDeck are no longer free.
## 3D models
| Name | URL | Free | License | Acct | MCP |
|---|---|---|---|---|---|
| Poly Haven | polyhaven.com | everything | CC0 | no | in mcp-for-blender |
| Poly Pizza | poly.pizza | 10.7k low-poly models | CC0 or CC-BY per model | no | in mcp-for-blender |
| Kenney | kenney.nl/assets | 200+ packs | CC0 | no | — |
| Quaternius | quaternius.com | about 90 packs, many rigged | Quaternius license: commercial use OK, no redistribution (**not CC0**) | no | — |
| Sketchfab | sketchfab.com | models under the "Downloadable" filter | CC per model | yes | in mcp-for-blender (API key). Now owned by KitBash (Aug 2026) |
| Blendkit (formerly BlenderKit) | blendkit.com | free plan: 23.8k models, 43.7k materials, 5.1k HDRIs | royalty-free / CC0 | yes | — |
| Fab (Epic) | fab.com | free drops that rotate every 2 weeks only; **Megascans are no longer free** | Fab Standard | Epic | — |
| Smithsonian 3D | 3d.si.edu | scans | CC0 only where marked | no | — |

## Textures and HDRI
- **ambientCG** (ambientcg.com): CC0, no account needed.
- **Poly Haven**: CC0.

## Animation and mocap
| Name | Free | License | Note |
|---|---|---|---|
| Mixamo (mixamo.com) | auto-rig plus animations | Adobe, royalty-free | fragile: no updates in years. Community MCP: V1xel/mixamo-mcp (5★) |
| CMU Mocap (mocap.cs.cmu.edu) | about 2,500 clips | free to copy, modify, redistribute | use http (TLS certificate error) |
| Rokoko (rokoko.com) | Starter plan: 30 s/month video-to-mocap, unlimited text-to-motion | royalty-free (UNVERIFIED) | FBX export |
| FreeMoCap (freemocap.org) | open-source markerless video-to-mocap | AGPL (UNVERIFIED) | 10.5k★, active. **Best free option for dance reference → rig** |
| ActorCore | small free set | Reallusion | mostly paid |
| ~~DeepMotion~~ | free tier is non-commercial | — | dropped |
| ~~Move One~~ | essentially no free tier | — | dropped |

## Footage
| Name | License | MCP |
|---|---|---|
| Pexels | commercial OK, no credit, no resale | garylab/pexels-mcp-server (27★) |
| Pixabay (images, video, music, SFX) | no credit, no standalone resale. **Music carries Content ID claim risk** | zym9863/pixabay-mcp (10★) |
| Mixkit | per-asset Mixkit license; some video is "Restricted" | — |
| Coverr | commercial OK. **No AI training** | — |
| NASA (images.nasa.gov) | generally public domain | API |
| Internet Archive / Prelinger | mostly public domain or CC, check each item | — |
| Openverse (openverse.org) | CC and public-domain search (images, audio) | neno-is-ooo/mcp-openverse (18★) |

## Audio and SFX
- **Freesound** (account needed). Licenses are CC0, CC-BY or **CC-BY-NC**, so filter by license. MCP: johnkimdw/freesound-mcp-server.
- **Pixabay audio**: see the Content ID note in the Footage table.
- **YouTube Audio Library**: now under Studio → Creator Music. Its license covers YouTube only.
- **Sonniss GDC bundle** (sonniss.com/gameaudiogdc): about 7.5 GB a year with an archive back to 2015. Royalty-free, no credit needed, **no AI training**.

## Fonts
- **Google Fonts**: OFL or Apache. The official **Google Design MCP** is at `https://design.googleapis.com/mcp` and needs Google Cloud auth. For Remotion, use `@remotion/google-fonts`.
- **Fontshare**: ITF Free Font License. Use their CDN; don't redistribute the font files.
- **Velvetyne**: OFL. The site currently shows a strike banner, and download status is UNVERIFIED.

## Motion
- **LottieFiles**: Lottie Simple License, account needed.
  - Official MCP: `https://mcp.lottiefiles.com/mcp` (OAuth). Whether it can search the public library is UNVERIFIED.
  - Community MCP that does public search: junmer/mcp-server-lottiefiles (19★).

## Reference and taste (reference only, never reuse frames)
- FILMGRAB (film-grab.com): active.
- Art of the Title.
- Motionographer.
- Vimeo Staff Picks.
- Recent (recent.design): godly.website now redirects here.
- Savee: free tier is capped.
- Mobbin: free tier is limited.
- Eyecannndy: whether it's free is UNVERIFIED.
- ~~ShotDeck~~: paid, dropped.

## AI video and tooling MCPs
| Name | Endpoint / install | Note |
|---|---|---|
| Runway (official, hosted) | `https://mcp.runwayml.com/mcp` (OAuth) | Gen-4.5, Kling 3.0, Veo 3.1. The old repo is archived |
| Higgsfield (official, hosted) | `https://mcp.higgsfield.ai/mcp` (OAuth); CLI is `higgsfield-ai/cli` | already connected for this user. Motion transfer: `hf_mult_motion_control` |
| Luma (official org) | lumalabs/luma-api-mcp | stale since 2025-04 |
| Kling | no official MCP | reach it through Runway or Higgsfield |
| mcp-for-blender (formerly ahujasid/blender-mcp) | `uvx mcp-for-blender` | 32.2k★, MIT. Pulls Poly Haven, Sketchfab and Poly Pizza; text/image to 3D |
| Blender Lab MCP (official) | projects.blender.org/lab/blender_mcp, Blender 5.1+ | **port 9876 clashes** with mcp-for-blender. Run only one |
| Unreal 5.8 MCP (official, experimental) | UE plugin | only for the recreate engine's UE branch |
| Remotion | `npx skills add remotion-dev/skills` (5.6k★); `@remotion/mcp` is docs lookup only | |
| HyperFrames | `npx skills add heygen-com/hyperframes` (71.4k★) | includes /music-to-video |

## MCP shortlist (ranked)
1. mcp-for-blender
2. HyperFrames and Remotion skills
3. Runway MCP
4. Higgsfield MCP
5. Blender Lab MCP (instead of #1, never alongside it)
6. Google Design MCP (fonts)
7. Freesound / Pexels MCPs (calling their APIs directly is a fine alternative)
8. Unreal 5.8 MCP

## Still unverified
- Eyecannndy free tier
- Poly Pizza API terms
- Mixamo's current terms
- Unreal MCP docs page
- LottieFiles official MCP public search
