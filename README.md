# Jörmungandr

A particle accelerator the size of the Earth, worked out with real physics.
One HTML file. No build step, no libraries.

**Live: https://patrikbartas.github.io/jormungandr/**

## What is in it

- **The ring.** A great circle, 40,030 km long, floating 200 m under the oceans.
- **The route.** `route.py` tests every great circle against the Natural Earth
  map and keeps the one that crosses the least land: 3,451 km (8.6%), against
  8,762 km along the equator. Its axis points at 23.98° N, 79.05° E.
- **The machine.** Pick a particle, the magnet field and the length of
  accelerating cavities. The page recomputes everything live.
- **Collisions.** Two beams run in opposite directions, gain energy lap by lap
  and are steered into each other at one of three bases.
- **The bases.** Named after the serpent's family: Loki (Northwest Territories,
  Canada), Fenrir (Casamance, Senegal) and Hel (Tasmania). Scroll to a base,
  point at it or click it on the globe to fly there.

With the default settings (8.33 T magnets, 400 km of cavities):

| Particle    | Top energy | Collision energy | Laps to get there | Time    |
|-------------|-----------:|-----------------:|------------------:|--------:|
| Protons     | 9.32 PeV   | 18.6 PeV         | 1,344             | 3.0 min |
| Electrons   | 5.08 TeV   | 10.2 TeV         | 0.73              | 98 ms   |
| Lead nuclei | 639 PeV    | 1.28 EeV         | 1,125             | 2.5 min |
| Muons       | 1.05 PeV   | 2.1 PeV          | 151               | 20 s    |

The LHC reaches 6.8 TeV per proton. Every particle is past 99.9999% of light
speed before it finishes its first lap; the rest of the ramp adds energy, not
speed. What stops the protons is not the magnets but their own synchrotron
radiation.

## Run it

Open `index.html` in a browser, or upload that one file to any host.

To recompute the route (downloads about 14 MB of map data on first run):

    uv run --with numpy --with pillow route.py

## Assumptions

- Earth is a sphere of radius 6,371 km.
- Magnets fill 80% of the ring. Cavities push at 30 MV/m.
- Beam current is 0.74 A, the LHC's bunch pattern all the way round.
- Top energy is the magnet limit or 99% of the energy where radiation loss
  equals cavity gain, whichever is lower.
- Lakes and Antarctic ice shelves count as land.
- Injection, beam stability, cooling and cost are ignored.
- The collision animation is a picture, not a simulation: the laps on screen
  stand for many real ones, and the tracks of the explosion are random.

The formulas are listed at the bottom of the page and in the first lines of
the script in `index.html`.

## Changelog

### v2

- Black and white design that follows the system's light or dark mode. Only
  the ring and the particles are in colour.
- Two beams instead of one. They spin up in opposite directions and collide.
- Three bases where the collision can happen: Loki, Fenrir and Hel.
- The globe flies to a base when you scroll to it, point at it or click it.
- A small explosion of particle tracks at the collision point.
- The run readout moved under the globe.

### v1

- The ring, the least-land route, the live machine numbers and a single bunch
  launch.

## Prompt test with Fable 5.2

Everything here was made by Claude Fable 5.2 in Claude Code (high effort) from
two prompts, plus one follow-up answer to confirm the name. The prompts,
translated from Slovak and shortened:

**Prompt 1 (v1)**

> Design a particle accelerator around the Earth and give it a cool name. Find
> the best route. On 50 m pylons or under water? Calculate which particles it
> can accelerate, to what energy, how long it takes and how many laps. Make an
> engaging interactive page with real maths and physics, one file if possible,
> simple code, in English. Put it in a public GitHub repo and record your usage
> in the readme.

**Prompt 2 (v2)**

> Add automatic dark and light mode, no switch. Drop the bluish look: black and
> white, with colour only for the particles, the ring or the bases. Add a
> collision of two particles that spin up faster and faster until they meet,
> with a small explosion animation. Propose two or three bases where it can
> happen and name them. Make the page more interactive: scrolling to a base
> zooms the globe there, and bases can be clicked or hovered. Add the second
> prompt, a changelog and the usage of this task to the readme. This is
> version 2. Commit and push.

Usage, read from the session log. Prompt 2 is counted up to its readme commit,
so its final push and summary are not included.

| | Prompt 1 | Prompt 2 |
|---|---:|---:|
| Wall time | 29 min, including the wait for the name | 10 min |
| API requests | 18 | 12 |
| Tool calls | 27 | 23 |
| Input tokens | 38 | 26 |
| Output tokens | 89,303 | 55,499 |
| Cache write tokens | 255,053 | 69,076 |
| Cache read tokens | 2,292,103 | 2,662,855 |
