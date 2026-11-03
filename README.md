<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <img alt="Andrew Mullen: AI researcher, quantum computing, energy professional with 10+ years in US gas and electric utilities, builder of robotics, scientific-computing and game projects." src="assets/banner-light.svg" width="100%">
</picture>

I'm Andrew, an AI researcher finishing an MSc on long-context LLM inference, with more than a decade in the
US gas & electric utility sector. I like problems where the answer has to hold up: proofs with
rigorous error bounds, swarms that have to keep flying, systems that must stay correct while getting faster.
Most of my work lives in private repositories, so the cards below show what each project does. Demos and
code walk-throughs are available on request.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-connect-0A66C2?style=flat-square)](https://www.linkedin.com/in/andrew-mullen-45152b251/)

## Research highlights

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero/drone-dark.svg">
  <img alt="Self-maintaining drone swarm: animated top-down view of six simulated Crazyflie drones in a room swept by four Lighthouse base stations, taking turns to fly and land on chargers. Positions come from the project's own simulator." src="assets/hero/drone-light.svg" width="100%">
</picture>

<details><summary><b>Self-maintaining drone swarm</b> · private · what it is</summary>

- Grew out of a University of Bern seminar brief on localization-quality-aware trajectory planning for aerial swarms.
- Localization-quality-aware planning, self-repair and decentralized control for a Lighthouse-tracked Crazyflie swarm designed to recharge itself (demonstrated in simulation so far).
- Tested in a custom simulator and in Gazebo running the real Crazyflie firmware (CrazySim); hardware flights come next.
</details>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero/navier-stokes-dark.svg">
  <img alt="Navier–Stokes collapse: animated chart of measured non-axisymmetric growth rates on Hou's collapsing Navier–Stokes state for two viscosities and modes m = 0, 1, 2, drawn from the paper's figure data, beside a schematic collapsing swirl." src="assets/hero/navier-stokes-light.svg" width="100%">
</picture>

<details><summary><b>Navier–Stokes collapse</b> · <a href="https://github.com/RavensStats/hou-front-stability">hou-front-stability</a> · what it is</summary>

- Paper: *A certified unstable eigenvalue of a columnar model of the front of Hou's Navier–Stokes collapse, and measured non-axisymmetric growth on the collapsing state*.
- The eigenvalue is proved by a computer-assisted (Plum-type) argument in verified interval arithmetic, with a Krawczyk enclosure of the discretized problem.
- Public code, figure data and a reproduction guide; companion private work solves for self-similar blowup profiles.
</details>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero/quantum-dark.svg">
  <img alt="Error-corrected quantum circuits: animated rotated surface code in which an error appears on a data qubit, two stabilizer checks light up as its syndrome and a decoder draws the correction, beside a scrolling syndrome-extraction circuit." src="assets/hero/quantum-light.svg" width="100%">
</picture>

<details><summary><b>Error-corrected quantum circuits</b> · private · what it is</summary>

- Research into fault-tolerant quantum computing with surface-code error correction.
- Works with benchmark circuits in OpenQASM and simulates how logical qubits detect and correct physical errors.
- The card above is a textbook illustration of the idea, not project output.
</details>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero/voice2vision-dark.svg">
  <img alt="Voice to Vision: animated illustration in which a waveform listens, three spoken phrases appear, and a picture of a cabin in the snow resolves from noise, turns to night and gains a deer." src="assets/hero/voice2vision-light.svg" width="100%">
</picture>

<details><summary><b>Voice to Vision</b> · private · what it is</summary>

- Speech goes through Whisper, then an LLM director, then SD-Turbo, and the picture is refined phrase by phrase while you talk.
- Code owns the state: the LLM only chooses among options the code offers, and clear cases are handled by fast local rules.
- A sibling tool, Voice to UI, builds working UI prototypes by voice and exports them as HTML.
</details>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/RavensStats/RavensStats/output/github-snake-dark.svg">
  <img alt="Animated contribution graph: a snake eats this year's GitHub contributions." src="https://raw.githubusercontent.com/RavensStats/RavensStats/output/github-snake.svg" width="100%">
</picture>

## More projects

<table>
<tr>
<td width="50%"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/tiles/thesis-dark.svg"><img alt="MSc thesis: context chunks flow into an LLM; cached chunks take a fast reuse lane, the rest are recomputed." src="assets/tiles/thesis-light.svg" width="100%"></picture>
<br><sub>Research · Python · PyTorch · Hugging Face · private</sub></td>
<td width="50%"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/tiles/final-platform-dark.svg"><img alt="The Final Platform: players hop up a procedural stack of platforms while a violet Void rises and erases the platforms below." src="assets/tiles/final-platform-light.svg" width="100%"></picture>
<br><sub>Game · Unity 6 · URP · Netcode · Steam · private</sub></td>
</tr>
<tr>
<td><picture><source media="(prefers-color-scheme: dark)" srcset="assets/tiles/battleblips-dark.svg"><img alt="Battleblips: three stacked hex layers; a sonar ping reveals a hidden enemy ship while a decoy flickers." src="assets/tiles/battleblips-light.svg" width="100%"></picture>
<br><sub>Game · Unity 6 · procedural meshes and shaders · private</sub></td>
<td><picture><source media="(prefers-color-scheme: dark)" srcset="assets/tiles/doodle-coaster-dark.svg"><img alt="Doodle-Coaster: a pencil sketches a coaster track, supports appear, then a cart rides it." src="assets/tiles/doodle-coaster-light.svg" width="100%"></picture>
<br><sub>Game · Unity · C# · private</sub></td>
</tr>
<tr>
<td><picture><source media="(prefers-color-scheme: dark)" srcset="assets/tiles/survivors-dark.svg"><img alt="Survivors-like: enemies converge on the hero and pop into XP gems against orbiting projectiles." src="assets/tiles/survivors-light.svg" width="100%"></picture>
<br><sub>Game · Unity · C# · private</sub></td>
<td><picture><source media="(prefers-color-scheme: dark)" srcset="assets/tiles/candy-kings-dark.svg"><img alt="Candy Kings: a purple candy army and a pink unicorn army face off; a thrown sweet inflates an enemy until it pops into confetti." src="assets/tiles/candy-kings-light.svg" width="100%"></picture>
<br><sub>Game · Unity 6 · 2D URP · local co-op · private</sub></td>
</tr>
<tr>
<td><a href="https://github.com/RavensStats/rosviz-web"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/tiles/rosviz-dark.svg"><img alt="ROSViz Web: a robot drives a route with a sweeping lidar fan beside live battery, velocity and alert panels." src="assets/tiles/rosviz-light.svg" width="100%"></picture></a>
<br><sub>App · team project · <a href="https://github.com/RavensStats/rosviz-web">rosviz-web</a> · Next.js · Three.js · ROS 2 · Docker</sub></td>
<td><a href="https://github.com/RavensStats/FantasyFootballScripts"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/tiles/fantasy-dark.svg"><img alt="Fantasy league pages: a standings table re-sorts week by week." src="assets/tiles/fantasy-light.svg" width="100%"></picture></a>
<br><sub>App · <a href="https://github.com/RavensStats/Rocket-Raccoon-Pod">league pages</a> (customized fork of league-page) · <a href="https://github.com/RavensStats/FantasyFootballScripts">scripts</a> · Svelte · Python</sub></td>
</tr>
</table>

## Toolbox

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![ROS 2](https://img.shields.io/badge/ROS_2-22314E?style=flat-square&logo=ros&logoColor=white)
![C#](https://img.shields.io/badge/C%23-512BD4?style=flat-square&logoColor=white)
![Unity](https://img.shields.io/badge/Unity-000000?style=flat-square&logo=unity&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=flat-square&logo=googlecloud&logoColor=white)

<sub>Every card is an animated SVG generated by <a href="tools/">tools/</a> (<code>python tools/build_cards.py</code>). The drone and Navier–Stokes cards are drawn from real project data.</sub>
