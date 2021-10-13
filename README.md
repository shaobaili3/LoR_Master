
# LoR Master Tracker-beta

<p align="center">
<img src="Preview/logo2.jpg"width="480" height="270"/>
</p>

<p align="center">
    <a href="https://github.com/shaobaili3/lor_master/releases"><img src="https://img.shields.io/github/v/release/shaobaili3/lor_master?include_prereleases"/></a>
    <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/language-Python-<COLOR>.svg"/></a>
    <a href="https://github.com/shaobaili3/LoR_Master/blob/master/LICENSE"><img src="https://img.shields.io/github/license/mashape/apistatus.svg"/></a>

</p>

LoR Master Tracker is a open source deck tracker for League of Runeterra.
<svg fill="none" viewBox="0 0 600 300" width="200" height="100" xmlns="http://www.w3.org/2000/svg">
	<foreignObject width="100%" height="100%">
		<div xmlns="http://www.w3.org/1999/xhtml">
			<style>
				@keyframes rotate {
					0% {
						transform: rotate(-3deg) translate3d(0, 0, 0);
					}
					100% {
						transform: rotate(1deg) translate3d(0, 1em, 0);
					}
				}
				@keyframes gradientBackground {
					0% {
						background-position: 0% 0%;
					}
					50% {
						background-position: 100% 100%;
					}
					100% {
						background-position: 0% 0%;
					}
				}
				@keyframes fadeIn {
					0% {
						opacity: 0;
					}
					66% {
						opacity: 0;
					}
					100% {
						opacity: 1;
					}
				}
				.container {
					font-family:
						system-ui,
						-apple-system,
						'Segoe UI',
						Roboto,
						Helvetica,
						Arial,
						sans-serif,
						'Apple Color Emoji',
						'Segoe UI Emoji';
					display: flex;
					flex-direction: column;
					align-items: center;
					justify-content: center;
					margin: 0;
					width: 100%;
					height: 400px;
					background-size: 600% 400%;
					animation: gradientBackground 10s ease infinite;
					border-radius: 10px;
					color: white;
					text-align: center;
				}
                h1:hover {
                    box-shadow:
						0 1px 0 #efefef,
						0 2px 0 #efefef,
						0 3px 0 #efefef,
						0 4px 0 #efefef,
						0 20px 8px rgba(0, 0, 0, 0.1);
                    cursor: pointer;
                }

                a {
                    color: white;
                    text-decoration: none;
                }

				h1 {

                    display: flex;

                    gap: 0.5em;

                    background: linear-gradient(-45deg, rgb(224, 171, 24), #fc5c7d, #6a82fb, #05dfd7);
                    background-size: 600% 400%;

                    border: 0.15em solid white;
                    padding: 0.8em 1em;
                    border-radius: 1em;
                    
                    box-shadow:
						0 1px 0 #efefef,
						0 2px 0 #efefef,
						0 3px 0 #efefef,
						0 4px 0 #efefef,
						0 12px 5px rgba(0, 0, 0, 0.1);

					font-size: 45px;

					line-height: 1.3;
					letter-spacing: 5px;
					animation: gradientBackground 12s ease infinite alternate;
				}

                h1 svg {
                    width: 1em;
                    display: block;
                }
				p {
					font-size: 20px;
					text-shadow: 0 1px 0 #efefef;
					animation: infinite alternate 1s fadeIn;
				}
			</style>
            
            <div class="container">
                <a href="https://github.com/shaobaili3/LoR_Master/releases/download/v0.9.14/LoRMasterTracker-Setup-0.9.14.exe">
                <h1>
                    <svg aria-hidden="true" focusable="false" data-prefix="fas" data-icon="download" class="svg-inline--fa fa-download fa-w-16" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="currentColor" d="M216 0h80c13.3 0 24 10.7 24 24v168h87.7c17.8 0 26.7 21.5 14.1 34.1L269.7 378.3c-7.5 7.5-19.8 7.5-27.3 0L90.1 226.1c-12.6-12.6-3.7-34.1 14.1-34.1H192V24c0-13.3 10.7-24 24-24zm296 376v112c0 13.3-10.7 24-24 24H24c-13.3 0-24-10.7-24-24V376c0-13.3 10.7-24 24-24h146.7l49 49c20.1 20.1 52.5 20.1 72.6 0l49-49H488c13.3 0 24 10.7 24 24zm-124 88c0-11-9-20-20-20s-20 9-20 20 9 20 20 20 20-9 20-20zm64 0c0-11-9-20-20-20s-20 9-20 20 9 20 20 20 20-9 20-20z"></path></svg>
                    Download</h1></a>
            </div>
		</div>
	</foreignObject>
</svg>
## [Download](https://github.com/shaobaili3/LoR_Master/releases/download/untagged-266d361330d2b4ae0f96/LoRMasterTracker-Setup-0.9.14.exe)
* Requirements: Windows 10 64bit
* [Click here to download](https://github.com/shaobaili3/LoR_Master/releases/download/untagged-266d361330d2b4ae0f96/LoRMasterTracker-Setup-0.9.14.exe)
* [Changelogs](https://github.com/shaobaili3/lor_master/releases)

## Features

* **Player Profile**

    Player Profile displays all your match history with analytical data.
![n](Preview/profile.png)

* **Player Inspector**

    By simply providing the player name, Player Inspector shows match history and statistics. Multiple Language player names are supported.
![n](Preview/inspect.png)

* **Deck Tracker**

    At the game beginning, players' decks, opponent history, rank, both graveyards and cards in hand number automatically revealed by real-time deck tracker.
![c](Preview/tracker2.png)
![c](Preview/tracker.png)   
    > ### Disclaimer:
    > Opponent history are pulled from recent 10 matches by [Riot API](https://developer.riotgames.com/apis). Riot suggested website [DAK.GG](https://dak.gg/lor) provides the same functionality. We are looking forward to getting feedback from the community and Riot.

* **Master Leaderboard**

    Master Leaderboard is powered by open-source [LMT Crawler](https://github.com/LoR-Master-Tracker/LoR-Player-Crawler). You can inspect master players via clicking player names.
![c](Preview/leaderboard.png)

* **Deck Code Viewer(Coming soon)**

    The deck viewer can be displayed in-game and outside the game via entering the deck codes.


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

2. Run Python Service

  ```shell
  pip install -r requirements.txt
  python LMTService.py
  ```

  If this errors out, make sure that you have an `Python3` environment
  variable pointing to the right path.

3. Run Electron User Interface

  ```shell
  cd UI
  npm install
  npm run dev
  ```

  Make sure you are in `UI` directory.

## FAQ

**Q.** Is using LoR Master Tracker considered cheating?  
**A.** This project is registered in the [Riot Development Portal](https://developer.riotgames.com/) and API keys are authorized by [Riot](https://www.riotgames.com/en). All data source is from [Riot API](https://developer.riotgames.com/apis) and [LoR Data Dragon](https://developer.riotgames.com/docs/lor). There is no third-party data source, API, and no local or remote database. all requests sent via our Riot API keys, all data cached locally.

### Built with ❤ by Storm & FlyingFish
