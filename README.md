<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <img alt="Andrew Mullen: energy and technology professional with 10+ years in US utilities; data and business analyst, software developer and test manager; AI, robotics and quantum computing research." src="assets/banner-light.svg" width="100%">
</picture>

I'm Andrew, an energy and technology professional with more than a decade in the US gas & electric
utility sector, working as a data & business analyst, software developer and test manager. I have a passion
for process improvement and IT transformation projects, and I research AI, robotics and quantum computing,
including an MSc thesis on long-context LLM inference. Most of my work lives in private repositories, so the
cards below show what each project does. Demos and code walk-throughs are available on request.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-connect-0A66C2?style=flat-square)](https://www.linkedin.com/in/andrew-mullen-45152b251/)

## Research highlights

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero/outage-risk-dark.svg">
  <img alt="Outage risk from short outages: animated card. A schematic drone ignores its positioning fixes while the base stations keep sweeping, and its estimate drifts away from the reference. Beside it, real offline data from one public-dataset flight: 127 short 1 to 1.5 s outages build a ladder of drift measurements, a 3 s abort limit is predicted from them, and 5 of 51 held-out 3 s outages exceed it, against 49 of 51 for a simulator's limit. Below, the share of held-out outages beyond each abort limit on six public datasets (target 10 %)." src="assets/hero/outage-risk-light.svg" width="100%">
</picture>

<details><summary><b>Outage risk from short outages</b> · private · what it is</summary>

- In flight the drone briefly stops passing its Lighthouse positioning to its estimator in flight while the positioning system keeps computing a reference from the same light, so drift (estimate − reference) is measured directly; a drone's own safe 1–1.5 s outages are used to predict its longer ones.
- Hardware lab days with Crazyflies are under way; the method has already been replicated offline on six public flight datasets.
- Offline, abort limits set from simulators with datasheet IMU noise are exceeded on 82–100 % of held-out 3 s outages (target 10 %), and with tracked-flight-fitted noise on 92–100 % for four of six datasets; limits from the drone's own short outages on 10–23 %.
</details>

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

<a href="https://github.com/Rikoleurt/ASE_Group3"><picture> <source media="(prefers-color-scheme: dark)" srcset="assets/hero/linear-a-dark.gif"> <img alt="Linear A Tablet Reader: demo recording in which a Minoan tablet drawing is uploaded, its signs are boxed and read, and the fraction check compares the entries with the KU-RO total." src="assets/hero/linear-a-light.gif" width="100%"> </picture></a>

<details><summary><b>Linear A Tablet Reader</b> · <a href="https://github.com/Rikoleurt/ASE_Group3">ASE_Group3</a> · what it is · full-resolution demo</summary>

- Upload a Linear A tablet drawing: a sign detector and a classifier (YOLO) locate the signs and propose readings, with hover details for each sign.
- Quantities and fractions are interpreted and checked against the KU-RO ("total") entry, showing whether the tablet's arithmetic balances.
- Vue frontend, FastAPI backend and a corpus-based reading view; Linear A is undeciphered, so the app reads signs and arithmetic, not language.

https://github.com/user-attachments/assets/a9dcaa56-567a-4865-9641-fb5758889c16

</details>

<a href="https://ravensstats.github.io/RavensStats/"><picture> <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/RavensStats/RavensStats/output/snake-dark.svg"> <img alt="Contribution snake: a snake crawls over the last year of GitHub contributions, eating each day with a commit and growing longer with every one." src="https://raw.githubusercontent.com/RavensStats/RavensStats/output/snake-light.svg" width="100%"> </picture></a>

<p align="center"><a href="https://ravensstats.github.io/RavensStats/"><img alt="Play Contribution Snake in your browser" src="https://img.shields.io/badge/%E2%96%B6%20PLAY-Contribution%20Snake-8250df?style=for-the-badge"></a></p>

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
<td><a href="https://store.steampowered.com/app/4841870/Hephaestus_Protocol/"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/tiles/hephaestus-protocol-dark.svg"><img alt="Hephaestus Protocol: a smith hammers at an anvil while forged blades orbit and mythic hordes converge and pop into XP gems." src="assets/tiles/hephaestus-protocol-light.svg" width="100%"></picture></a>
<br><a href="https://store.steampowered.com/app/4841870/Hephaestus_Protocol/"><img alt="Hephaestus Protocol on Steam" src="https://img.shields.io/badge/Hephaestus%20Protocol-171a21?style=flat-square&logo=steam&logoColor=white"></a> <sub>Game · Unity 6 · C#</sub></td>
<td><picture><source media="(prefers-color-scheme: dark)" srcset="assets/tiles/candy-kings-dark.svg"><img alt="Candy Kings: a purple candy army and a pink unicorn army face off; a thrown sweet inflates an enemy until it pops into confetti." src="assets/tiles/candy-kings-light.svg" width="100%"></picture>
<br><sub>Game · Unity 6 · 2D URP · local co-op · private</sub></td>
</tr>
<tr>
<td><a href="https://github.com/RavensStats/rosviz-web"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/tiles/rosviz-dark.svg"><img alt="ROSViz Web: a robot drives at a wall; the safety monitor warns, goes critical and auto-stops it, then clears the alert, with alerts streamed to the dashboard and Grafana." src="assets/tiles/rosviz-light.svg" width="100%"></picture></a>
<br><sub>App · <a href="https://github.com/RavensStats/rosviz-web">rosviz-web</a> · ROS 2 · Prometheus · Grafana · Next.js · Docker</sub></td>
<td><a href="https://github.com/RavensStats/FantasyFootballScripts"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/tiles/fantasy-dark.svg"><img alt="Fantasy league pages: a standings table re-sorts week by week." src="assets/tiles/fantasy-light.svg" width="100%"></picture></a>
<br><sub>App · <a href="https://github.com/RavensStats/Rocket-Raccoon-Pod">league pages</a> (customized fork of league-page) · <a href="https://github.com/RavensStats/FantasyFootballScripts">scripts</a> · Svelte · Python</sub></td>
</tr>
<tr>
<td><picture><source media="(prefers-color-scheme: dark)" srcset="assets/tiles/proth-prime-search-dark.svg"><img alt="Proth Prime Search: the first 240 odd k of k·2^332,200,000 + 1 on a grid; waves of primes q = 3, 5, 7, … knock out every k with that factor, using the project's real sieve data, until the 10 true survivors remain glowing." src="assets/tiles/proth-prime-search-light.svg" width="100%"></picture>
<br><sub>Research · C · Python · Oracle Cloud · private</sub></td>
<td><a href="https://github.com/MateoLopez00/SafeSplit_Distributed_DL"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/tiles/backdoor-robustness-dark.svg"><img alt="Backdoor attacks and defences: four clients send activations through a U-shaped split model (client head, server backbone, client tail); one client's image carries a red trigger patch, its checkpoint is flagged suspicious and rolled back to the last benign one, and the client gets a low-trust flag. Numbers are SafeSplit's backdoor accuracy without vs with the defence, from the reproduction's README." src="assets/tiles/backdoor-robustness-light.svg" width="100%"></picture></a>
<br><sub>Research · <a href="https://github.com/MateoLopez00/SafeSplit_Distributed_DL">SafeSplit reproduction</a> (NDSS 2025) · <a href="https://github.com/MateoLopez00/DL-Backdoor-Attacks-and-Robustness-in-Training">DL course project</a> · Python · PyTorch · CIFAR-10</sub></td>
</tr>
<tr>
<td><a href="https://github.com/RavensStats/PokemonRedExperiments"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/tiles/pokemon-red-rl-dark.svg"><img alt="Pokémon Red RL experiments: an agent explores a tile map while a coverage heat map fills in behind it, story-event, battle and heal rewards pop as it reaches them, and the coverage bar and shaped-reward curve rise." src="assets/tiles/pokemon-red-rl-light.svg" width="100%"></picture></a>
<br><sub>Research · <a href="https://github.com/RavensStats/PokemonRedExperiments">PokemonRedExperiments</a> (fork of PWhiddy's) · Python · PyBoy · Stable-Baselines3 PPO</sub></td>
<td><a href="https://github.com/rachelyongies/diffusion_model_quantization"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/tiles/diffusion-quantization-dark.svg"><img alt="Diffusion model quantization: a picture denoises out of random noise four times, as FP16, INT8, INT4 and INT8 with fewer steps, while a histogram of UNet activations stays smooth at 8 bits and snaps onto 16 levels at 4 bits. The table gives the notebook's measured seconds per image and CLIPScore for each mode: fake quantization alone is slower than FP16, INT4 loses quality, and cutting to 20 steps gives a 27 % latency cut." src="assets/tiles/diffusion-quantization-light.svg" width="100%"></picture></a>
<br><sub>Research · <a href="https://github.com/rachelyongies/diffusion_model_quantization">diffusion_model_quantization</a> · Python · PyTorch · diffusers</sub></td>
</tr>
<tr>
<td><a href="https://github.com/RavensStats/2D-Escape-Room"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/tiles/escape-room-dark.svg"><img alt="Escape Room: in a bedroom scene a cursor reads a note, sets a four-slider light puzzle to its solution, finds two key parts in a drawer and under the bed, combines them into a key and unlocks the door." src="assets/tiles/escape-room-light.svg" width="100%"></picture></a>
<br><sub>Game · Unity 6 · C# · <a href="https://github.com/RavensStats/2D-Escape-Room">2D-Escape-Room</a> · <a href="https://github.com/RavensStats/Escape-Room">3D prototype</a></sub></td>
<td><picture><source media="(prefers-color-scheme: dark)" srcset="assets/tiles/classic-games-dark.svg"><img alt="Classic Games: a spinning disc streams into a Windows 10/11 window, compatibility fixes tick off one by one (proxy DLL hooks, no-CD, DirectDraw, AVI video, window scaling) and an abstract answer-the-sum shooter starts running." src="assets/tiles/classic-games-light.svg" width="100%"></picture>
<br><sub>Retro · C · Win32 · proxy DLLs · PowerShell · private</sub></td>
</tr>
<tr>
<td><picture><source media="(prefers-color-scheme: dark)" srcset="assets/tiles/heroclix-manual-dark.svg"><img alt="HeroClix: on a square-grid map a figure moves three squares, traces a line of fire to an enemy, rolls 2d6 against its defense and hits, and the target's combat dial clicks twice as its values drop." src="assets/tiles/heroclix-manual-light.svg" width="100%"></picture>
<br><sub>Game · Unity 6 · C# · PHP/MySQL server · private</sub></td>
<td><picture><source media="(prefers-color-scheme: dark)" srcset="assets/tiles/tictactoe-evolved-dark.svg"><img alt="Tic Tac Toe Evolved: one board plays through four of the game's eight modes in turn: Classic (X wins the top row), Gravity (marks drop to the column floor), Quantum (older marks fade and each player's fourth mark erases their oldest) and Expansion (a new column grows after each move), while the mode list highlights the active variant." src="assets/tiles/tictactoe-evolved-light.svg" width="100%"></picture>
<br><sub>Game · Unity 6 · C# · private</sub></td>
</tr>
<tr>
<td><picture><source media="(prefers-color-scheme: dark)" srcset="assets/tiles/guess-who-dark.svg"><img alt="Guess Who: a board of 24 abstract face cards; yes/no questions about hats, glasses, beards and hair flip the non-matching cards down one question at a time until a single card is left and the guess is right." src="assets/tiles/guess-who-light.svg" width="100%"></picture>
<br><sub>Game · Unity 6 · C# · private</sub></td>
<td><a href="https://github.com/RavensStats/hou-front-stability"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/tiles/navier-stokes-dark.svg"><img alt="Navier–Stokes collapse: measured non-axisymmetric growth rates on Hou's collapsing Navier–Stokes state for two viscosities and modes m = 0, 1, 2 draw in, from the paper's public figure data." src="assets/tiles/navier-stokes-light.svg" width="100%"></picture></a>
<br><sub>Research · <a href="https://github.com/RavensStats/hou-front-stability">hou-front-stability</a> · Python · interval arithmetic</sub></td>
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
![C](https://img.shields.io/badge/C-A8B9CC?style=flat-square&logo=c&logoColor=black)
![PHP](https://img.shields.io/badge/PHP-777BB4?style=flat-square&logo=php&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)
![Svelte](https://img.shields.io/badge/Svelte-FF3E00?style=flat-square&logo=svelte&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js-4FC08D?style=flat-square&logo=vuedotjs&logoColor=white)

<sub>Every card is generated by <a href="tools/">tools/</a>: animated SVGs from <code>python tools/build_cards.py</code>, and the Linear A card as a looping GIF of its demo recording (<code>tools/build_linear_a.py</code>). The drone, outage-risk (drift data; its drone scene is schematic), Navier–Stokes and Proth Prime Search cards are drawn from real project data.</sub>
