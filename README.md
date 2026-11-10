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

With the default settings (8.33 T magnets, 400 km of cavities):

| Particle    | Top energy | Laps to get there | Time    |
|-------------|-----------:|------------------:|--------:|
| Protons     | 9.32 PeV   | 1,344             | 3.0 min |
| Electrons   | 5.08 TeV   | 0.73              | 98 ms   |
| Lead nuclei | 639 PeV    | 1,125             | 2.5 min |
| Muons       | 1.05 PeV   | 151               | 20 s    |

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

The formulas are listed at the bottom of the page and in the first lines of
the script in `index.html`.

## Single-prompt Fable 5.2 test

Everything here was made by Claude Fable 5.2 in Claude Code from one prompt,
plus one follow-up answer to confirm the name. The prompt, translated from
Slovak and shortened:

> Design a particle accelerator around the Earth and give it a cool name. Find
> the best route. On 50 m pylons or under water? Calculate which particles it
> can accelerate, to what energy, how long it takes and how many laps. Make an
> engaging interactive page with real maths and physics, one file if possible,
> simple code, in English. Put it in a public GitHub repo and record your usage
> in the readme.

Usage, read from the session log just before the final commit:

| | |
|---|---|
| Model | claude-fable-5-2, high effort |
| Wall time | 24 minutes, including the wait for the name |
| API requests | 14 |
| Tool calls | 24 |
| Input tokens | 30 |
| Output tokens | 85,224 |
| Cache write tokens | 248,918 |
| Cache read tokens | 1,609,861 |
