
# LoR Master Tracker-beta

<p align="center">
<img src="Preview/logo2.jpg"width="480" height="270"/>
</p>

<p align="center">
    <a href="https://github.com/shaobaili3/lor_master/releases"><img src="https://img.shields.io/github/v/release/shaobaili3/lor_master?include_prereleases"/></a>
    <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/language-Python-<COLOR>.svg"/></a>
    <a href="https://github.com/shaobaili3/LoR_Master/blob/master/LICENSE"><img src="https://img.shields.io/github/license/mashape/apistatus.svg"/></a>

</p>

LoR Master Tracker is a open source match tracker and player inspector for League of Runeterra.

## [Download](https://github.com/shaobaili3/LoR_Master/releases/download/v0.9.7.2-beta/LoRMasterTracker-v0.9.7.2-beta.exe)

* Requirements: Windows 7 or higher
* [Click here to download](https://github.com/shaobaili3/LoR_Master/releases/download/v0.9.7.2-beta/LoRMasterTracker-v0.9.7.2-beta.exe)
* [Changelogs](https://github.com/shaobaili3/lor_master/releases)

## Features

* **Player Inspector**

    By simply providing the player name, LMT can inspect match history. Multiple Language player names are supported.
![n](Preview/inspect.png)

* **In-game Deck Tracker**

    At the game beginning, players' decks, opponent history, rank and both graveyards automatically revealed by real-time deck tracker.
![c](Preview/tracker2.png)
![c](Preview/tracker.png)   
    > ### Disclaimer:
    > Opponent history are pulled from recent 10 matches by [Riot API](https://developer.riotgames.com/apis). We are looking forward to getting feedback from the community and Riot.

* **Real time Master Leaderboard**

    LMT real-time master leaderboard is powered by open-source [LMT Crawler](https://github.com/LoR-Master-Tracker/LoR-Player-Crawler). You can inspect master players via clicking player names.
![c](Preview/leaderboard.png)

* **In-game Deck Code Viewer(Coming soon)**

    LMT can view the deck by entering the deck code. The viewer can be displayed in-game.





## Development

LoR Master Tracker backend service is written by [Python3](https://www.python.org). The user interface is built by [Electron](https://www.electronjs.org/) and [Vuejs](https://github.com/vuejs/vue)

## Build Instructions

Pre-requisites:

* To run command line tools, you'll need to configure Python3
* npm

1. Clone or Download the repository:

  ```shell
  git clone https://github.com/shaobaili3/LoR_Master
  ```

2. Run Python backend + main UI

  ```shell
  pip install -r requirements.txt
  python LoRMasterTracker.py
  ```

  If this errors out, make sure that you have an `Python3` environment
  variable pointing to the right path.

3. Run Electron in-game UI

  ```shell
  cd UI
  npm install
  npm run dev
  npm run package
  ```

  Make sure you are in `UI` directory.

## FAQ

**Q.** Is using LoR Master Tracker considered cheating?  
**A.** This project is registered in the [Riot Development Portal](https://developer.riotgames.com/) and the API key is proved by [Riot](https://www.riotgames.com/en). All data source is from [Riot API](https://developer.riotgames.com/apis) and [LoR Data Dragon](https://developer.riotgames.com/docs/lor). There is zero third-party data source and no third-party API.

### Built with ❤ by Storm & FlyingFish
