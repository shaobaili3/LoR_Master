# Legends of Runeterra Deck Tracker - LoR Master Tracker

<p align="center">
<img src="Preview/logo2.jpg"width="480" height="270"/>
</p>

<p align="center">
    <a href="https://github.com/shaobaili3/lor_master/releases"><img src="https://img.shields.io/github/v/release/shaobaili3/lor_master?include_prereleases"/></a>
    <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/language-Python-<COLOR>.svg"/></a>
    <a href="https://github.com/shaobaili3/LoR_Master/blob/master/LICENSE"><img src="https://img.shields.io/github/license/mashape/apistatus.svg"/></a>
    <a href="https://lormaster.com/"><img src="https://img.shields.io/github/downloads/shaobaili3/lor_master/total.svg"/></a>

</p>

[LoR Master Tracker](https://app.lormaster.com/) is a open source deck tracker for League of Runeterra.
符文之地魔盒是一款开源LoR记牌器

- [Download](https://lormaster.com/)
- [Preview](https://app.lormaster.com/)
- [Changelogs](https://github.com/shaobaili3/lor_master/releases)

## [Features](https://app.lormaster.com/)

- **Deck Tracker**

- **Player Inspection**

- **Leaderboard**

- **Deck Library**

- **Meta Environment**


## Development

LoR Master Tracker's user interface is built by [Electron](https://www.electronjs.org/) and [Vuejs](https://github.com/vuejs/vue), and backend service is written by [Python 3](https://www.python.org). 

## Build Instructions

1. Install python3 and npm

2. Clone or Download the repository:

```shell
git clone https://github.com/shaobaili3/LoR_Master
```

3. Run Python Service

```shell
pip install -r requirements.txt
python LMTService.py
```

If this errors out, make sure that you have an `Python3` environment
variable pointing to the right path.

4. Run Electron User Interface

```shell
cd UI
npm install

// This will start a server. Served page can be accessed directly using browser as Web app version
npm run serve

// this will start Electron, accessing that served page but as Electron App version
npm run dev
```

Make sure you are in `UI` directory.

5. Bundle the Python service and Electron user interface into a single package.

The installer is automatically generated and released by CDCI on [Github Action](https://github.com/shaobaili3/LoR_Master/actions). Please refer to [python-app.yml](.github/workflows/node.js.yml)


## FAQ

**Q.** Is using LoR Master Tracker considered cheating?  
**A.** This project is approved by [Riot](https://www.riotgames.com/en/DevRel/rso), and registered in the [Riot Development Portal](https://developer.riotgames.com/). All data source is from [Riot API](https://developer.riotgames.com/apis) and [LoR Data Dragon](https://developer.riotgames.com/docs/lor). There is **NO** third-party data source.

### Built with ❤ by Storm & FlyingFish
