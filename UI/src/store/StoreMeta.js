const requestWaitTime = 1000 // ms
import axios from "axios"

import { defineStore } from "pinia"
import { useBaseStore } from "./StoreBase"

export const timeOptionsUrl = ["", "/1", "/3", "/7"]

export const regionOptionsUrl = ["/all", "/americas", "/europe", "/apac"]

export const useMetaStore = defineStore("meta", {
  state: () => {
    return {
      request: null,
      metaGroups: [],
      metaUpdateTime: null,
      lastRequestTime: null,
      isMetaLoading: true,
      timeOption: 0,
      regionOption: 0,
      totalMatches: 0,
      version: "",
    }
  },
  actions: {
    cancelRequest() {
      if (this.request) this.request.cancel()
    },
    fetchMetaGroups() {
      this.lastRequestTime = Date.now()
      this.isMetaLoading = true

      if (this.request) this.cancelRequest()
      const axiosSource = axios.CancelToken.source()
      this.request = { cancel: axiosSource.cancel, msg: "Loading..." }
      const baseStore = useBaseStore()

      var api_link = `${baseStore.API_WEB}/archetypes${regionOptionsUrl[this.regionOption]}${
        timeOptionsUrl[this.timeOption]
      }`

      // var promise = new Promise(resolve => setTimeout(resolve, 1000))
      var promise = axios.get(api_link, { cancelToken: axiosSource.token })
      promise
        .then((res) => {
          this.isMetaLoading = false
          if (res && res.data) {
            if (res.data.data) {
              this.metaGroups = res.data.data // res.data
              this.metaUpdateTime = res.data.time
              this.totalMatches = res.data.match_num
              if (res.data.version) {
                this.version = res.data.version
              }
            } else {
              this.metaGroups = res.data
            }
          } else {
            throw Error("Meta api response invalid")
          }
        })
        .catch((e) => {
          if (axios.isCancel(e)) {
            console.log("Request cancelled")
          } else {
            console.log("error", e)
            var elapsedTime = Date.now() - this.lastRequestTime // ms
            if (elapsedTime > requestWaitTime) {
              setTimeout(() => {
                this.fetchMetaGroups()
              }, 100)
            } else {
              setTimeout(() => {
                this.fetchMetaGroups()
              }, requestWaitTime - elapsedTime)
            }
          }
        })
    },
  },
})

const testData = [
  {
    _id: "faction_BandleCity_Name faction_Bilgewater_Name Nami Twisted Fate",
    play_num: 915,
    play_rate: 0.06709194896612407,
    win_rate: 0.5535714285714286,
    match_num: 877,
    decks: [
      {
        play_num: 301,
        deck_code: "CQCACAYGCEBAEBQYDIBAKBQFBMDQKCQBAQNCQMNGAG6ACAQBAUFMMAIBAUDACAA",
        win_rate: 0.5548172757475083,
        play_rate: 0.34321550741163054,
      },
      {
        play_num: 77,
        deck_code: "CQCACAYGCEBAEBQYDIBAKBQFBMDAKCQEDIUDDJQBXQAQCAQFBIA4MAIDAEBAMKQBAQDAUAIFBKTQC",
        win_rate: 0.44155844155844154,
        play_rate: 0.08779931584948689,
      },
      {
        play_num: 69,
        deck_code: "CQCACAYGCEBAEBQYDIBAKBQFBMDQKCQEDIUDDJQBXQA4MAIBAECQUAICAECAMCQBAUFKOAI",
        win_rate: 0.6666666666666666,
        play_rate: 0.07867730900798175,
      },
      {
        play_num: 56,
        deck_code: "CQCACAYGCEBAEBQYDIBAKBQFBMDAKCQEDIUDDJQBXQAQGAIEAYFACBIKYYAQCBIGAEAQCAQGFI",
        win_rate: 0.42857142857142855,
        play_rate: 0.06385404789053592,
      },
      {
        play_num: 38,
        deck_code: "CQCACAYGCEBAEBQYDIBAKBQFBMDAKCQEDIUDDJQBXQAQEAIFAYAQEBIKAHDACAIBAQDAU",
        win_rate: 0.631578947368421,
        play_rate: 0.043329532497149374,
      },
    ],
    matchup: [
      {
        _id: "faction_BandleCity_Name faction_ShadowIsles_Name Senna Veigar",
        match_num: 50,
        win_num: 20,
        win_rate: 0.4,
      },
      {
        _id: "faction_Demacia_Name faction_MtTargon_Name Pantheon",
        match_num: 48,
        win_num: 17,
        win_rate: 0.3541666666666667,
      },
      {
        _id: "faction_Ionia_Name faction_Piltover_Name Ahri Lulu",
        match_num: 41,
        win_num: 23,
        win_rate: 0.5609756097560976,
      },
      {
        _id: "faction_Ionia_Name faction_Shurima_Name Ahri Kennen",
        match_num: 40,
        win_num: 23,
        win_rate: 0.575,
      },
    ],
    players: [
      {
        _id: "s07aGy1D4pzNemWCIqZuboZOR_DayP4JXaKRpUWZ9YMJAACYEhqtFIEILT4ZVPPra7dm2VvmPpIEiA",
        count: 41.0,
        win_num: 29,
        win_rate: 0.7073170731707317,
        riot_id: "Spoogy#9001",
        server: "europe",
      },
      {
        _id: "q4PxbUI1gWnsTxXKbX9Kb137Qx90RDxRrHbMQxXqmaJqNyBk9dJe6AGfo9jNGlFpxCJ2-LsFSctnmw",
        count: 32.0,
        win_num: 13,
        win_rate: 0.40625,
        riot_id: "mtucks#OCE",
        server: "americas",
      },
      {
        _id: "yOv-HEBVyhs3et0mefNwb7aoZ_Y6T3OelYvbQiauuJPG5BDNw8Qr_b2FrljwbtXlt6DGKE1bC1fOHg",
        count: 27.0,
        win_num: 15,
        win_rate: 0.5555555555555556,
        riot_id: "o5wtf#2438",
        server: "europe",
      },
      {
        _id: "9i2iMs8ni3mmftaepc4gmbp6GixuO_MWc9Akl3fujEzZ6Wfxjzyeujca4YHPIIcJZUpdAlYkFdMq0Q",
        count: 27.0,
        win_num: 13,
        win_rate: 0.48148148148148145,
        riot_id: "Kuako#NA1",
        server: "americas",
      },
      {
        _id: "NbvNFFtwVtAMZK_HiQWh3hbdIYJ6mKUKQmRMLHGl5e5BUUj3wqALl4tzx4wIgEgorv0YkVoMoAXWqQ",
        count: 26.0,
        win_num: 13,
        win_rate: 0.5,
        riot_id: "Lumus11#12345",
        server: "americas",
      },
    ],
  },
  {
    _id: "faction_BandleCity_Name faction_ShadowIsles_Name Senna Veigar",
    play_num: 698,
    play_rate: 0.051180525003666225,
    win_rate: 0.5105421686746988,
    match_num: 681,
    decks: [
      {
        play_num: 59,
        deck_code: "CQBQCAIFFABAKBIIBEDAKCRRHFOV4YVGAEBAEAIFCMOQIBIKAENMMAORAEAQCAIFB4",
        win_rate: 0.6610169491525424,
        play_rate: 0.08663729809104258,
      },
      {
        play_num: 44,
        deck_code: "CQCACAIFFAAQGBIQAMCQKCAJBYCAKCQ2HFOWEAQDAECQ6EY5AMCQUAK6UYAQCAIFAUFA",
        win_rate: 0.5,
        play_rate: 0.06461086637298091,
      },
      {
        play_num: 39,
        deck_code: "CQBQEAIFDUUAEBIFBAEQSBIKAECBUMJZLVPGFJQBAAAQCAIFCQ",
        win_rate: 0.5384615384615384,
        play_rate: 0.05726872246696035,
      },
      {
        play_num: 34,
        deck_code: "CQBQCAIFFABAKBIIBEEAKCQ2GE4V2XTCUYA5CAIBAECQVGABAIBAKCQBYYAQGAIFCQOS4",
        win_rate: 0.47058823529411764,
        play_rate: 0.049926578560939794,
      },
      {
        play_num: 28,
        deck_code: "CQBQCAIFFABAKBIIBEDQKCQBGE4V2XTCUYAQEAIBAUOQCBIKDIBQCBAFHABAKCTKZUAQGAIFCMKCE",
        win_rate: 0.5,
        play_rate: 0.041116005873715125,
      },
    ],
    matchup: [
      {
        _id: "faction_BandleCity_Name faction_Bilgewater_Name Nami Twisted Fate",
        match_num: 50,
        win_num: 30,
        win_rate: 0.6,
      },
      {
        _id: "faction_Piltover_Name faction_Shurima_Name Ekko Zilean",
        match_num: 35,
        win_num: 15,
        win_rate: 0.42857142857142855,
      },
      {
        _id: "faction_Demacia_Name faction_MtTargon_Name Pantheon",
        match_num: 35,
        win_num: 12,
        win_rate: 0.34285714285714286,
      },
      {
        _id: "faction_Bilgewater_Name faction_Shurima_Name Pyke Rek'Sai",
        match_num: 34,
        win_num: 8,
        win_rate: 0.23529411764705882,
      },
    ],
    players: [
      {
        _id: "fUdGuh4-YKxPviz7uO2pqoLjSySoPP6KATlBf1Ldvviiw6SEltkX-oK0VEx9tq3QCWCs8g7l-9GvHg",
        count: 60.0,
        win_num: 26,
        win_rate: 0.43333333333333335,
        riot_id: "Venndulum#1119",
        server: "americas",
      },
      {
        _id: "LR2wIXPg2VUT9renvTTW1SaCxpCkdMk52E1ni0g7XCn3u02pcn4LZfM4FQCe5e9CVZv2IbeT-4I1AQ",
        count: 58.0,
        win_num: 32,
        win_rate: 0.5517241379310345,
        riot_id: "DSKINPISKCOOL#1071",
        server: "asia",
      },
      {
        _id: "AnJrb-aeam7fUqokyUAgsbuURA1mkVIFnWBYaL5vigoMngGdot2OR3eTUxNC8O0wKYoDFKd4dKiLxg",
        count: 55.0,
        win_num: 32,
        win_rate: 0.5818181818181818,
        riot_id: "kuzmoti#JP1",
        server: "asia",
      },
      {
        _id: "80f_lCbvFSoC419Y4vy1rFE2kGKhBlxAbQjxwYZ-oB1gF-32VkKjJnjqCcDNtnqP8i8B57vn3H-3cA",
        count: 40.0,
        win_num: 26,
        win_rate: 0.65,
        riot_id: "BBG#CCJY9",
        server: "americas",
      },
      {
        _id: "m4G-nJuqMK1dc7mQb8kTvHzFNwJddCTFpnn3B0ckbG-bH5Rrz77QSK0FqkIWX9JqrgOrtJwWiies6A",
        count: 35.0,
        win_num: 21,
        win_rate: 0.6,
        riot_id: "Tangled Forever #NA1",
        server: "americas",
      },
    ],
  },
  {
    _id: "faction_Demacia_Name faction_MtTargon_Name Pantheon",
    play_num: 630,
    play_rate: 0.046194456665200175,
    win_rate: 0.5929054054054054,
    match_num: 611,
    decks: [
      {
        play_num: 258,
        deck_code: "CICQCAYABYAQIAADAMAQACINDIBQKCIDAUDAIAYJDMRTGXABAEBAAAICAEBQSEYBAQAAE",
        win_rate: 0.5348837209302325,
        play_rate: 0.42225859247135844,
      },
      {
        play_num: 50,
        deck_code: "CICQCAYABYAQIAADAMAQACINDIBQKCIDAUDAIAYJDMRTGXACAEBAAAIBAQAAEAA",
        win_rate: 0.76,
        play_rate: 0.08183306055646482,
      },
      {
        play_num: 35,
        deck_code: "CICQCAYABYAQIAADAMAQACINDIBQKCIDAUDAIAYJDMRTGXACAEBAAAIBAMEWAAA",
        win_rate: 0.6,
        play_rate: 0.057283142389525366,
      },
      {
        play_num: 27,
        deck_code: "CICQCAYABYAQIAADAIAQADI2AMCQSAYFAYCAGCI3EMZVYAQBAEAASAQDBEJWEAIBAIAAC",
        win_rate: 0.7407407407407407,
        play_rate: 0.044189852700491,
      },
      {
        play_num: 24,
        deck_code: "CICQCAYABYAQIAADAMAQACINDIBQKCIDAUDAIAYJDMRTGXABAEBAAAICAEBQSEYBAUEQU",
        win_rate: 0.5416666666666666,
        play_rate: 0.03927986906710311,
      },
    ],
    matchup: [
      {
        _id: "faction_BandleCity_Name faction_Bilgewater_Name Nami Twisted Fate",
        match_num: 48,
        win_num: 31,
        win_rate: 0.6458333333333334,
      },
      {
        _id: "faction_BandleCity_Name faction_ShadowIsles_Name Senna Veigar",
        match_num: 35,
        win_num: 23,
        win_rate: 0.6571428571428571,
      },
      {
        _id: "faction_Piltover_Name faction_Shurima_Name Ekko Zilean",
        match_num: 33,
        win_num: 26,
        win_rate: 0.7878787878787878,
      },
      {
        _id: "faction_Ionia_Name faction_Shurima_Name Ahri Kennen",
        match_num: 30,
        win_num: 14,
        win_rate: 0.4666666666666667,
      },
    ],
    players: [
      {
        _id: "9i2iMs8ni3mmftaepc4gmbp6GixuO_MWc9Akl3fujEzZ6Wfxjzyeujca4YHPIIcJZUpdAlYkFdMq0Q",
        count: 76.0,
        win_num: 39,
        win_rate: 0.5131578947368421,
        riot_id: "Kuako#NA1",
        server: "americas",
      },
      {
        _id: "kvOdpb180wssuJDFhY3DMmJTFBwswXfR4qPqJpDHLNPDx-7-36-ZPUYltstjZM7_4HACxZyC5wbyOA",
        count: 37.0,
        win_num: 22,
        win_rate: 0.5945945945945946,
        riot_id: "nalkpas#NA1",
        server: "americas",
      },
      {
        _id: "yOv-HEBVyhs3et0mefNwb7aoZ_Y6T3OelYvbQiauuJPG5BDNw8Qr_b2FrljwbtXlt6DGKE1bC1fOHg",
        count: 24.0,
        win_num: 12,
        win_rate: 0.5,
        riot_id: "o5wtf#2438",
        server: "europe",
      },
      {
        _id: "fN0-OQHGyTxHvtJJo7MaRKPX2nq3BfwkOPhWIdHvJ-cwtZqrlEim1IkLZikqnO1vXR_ZLdFRXL7QVw",
        count: 20.0,
        win_num: 17,
        win_rate: 0.85,
        riot_id: "Bman#ETJ53",
        server: "americas",
      },
      {
        _id: "hV3BH94gkZFNtHT1dnK7kMRdi2A5_Jgsp44c46iW-8yeWxWJ6M1sBwFnzYyFfNbLPdBNWdQT6epKLQ",
        count: 20.0,
        win_num: 15,
        win_rate: 0.75,
        riot_id: "Ahuizotle#1234",
        server: "europe",
      },
    ],
  },
  {
    _id: "faction_Ionia_Name faction_Shurima_Name Ahri Kennen",
    play_num: 586,
    play_rate: 0.042968177152075085,
    win_rate: 0.6171328671328671,
    match_num: 579,
    decks: [
      {
        play_num: 100,
        deck_code: "CQCQCAYCAUAQIAQPAECQUOQCAUBAIGQGAEBAQCYMFQZDSAYBAMBBIAIEA6FACAIFAIKQCAIBAIYQ",
        win_rate: 0.71,
        play_rate: 0.17271157167530224,
      },
      {
        play_num: 64,
        deck_code:
          "CQDACAQCBIAQIAQPAECQUOQBAUBAIAQDAICRIBABAIFQYLBSAMAQIB4KAEAQKAQ2AIAQEMJZAIAQCAQIAECAEBY",
        win_rate: 0.640625,
        play_rate: 0.11053540587219343,
      },
      {
        play_num: 59,
        deck_code:
          "CQCQCAYCAUAQIAQPAECQUOQDAEBAWDBSAMCQEBAVDICACAQCAUAQGAQUAECAPCQBAMAQECBMGEAQCBICA4",
        win_rate: 0.6440677966101694,
        play_rate: 0.10189982728842832,
      },
      {
        play_num: 31,
        deck_code:
          "CQDACAQCBIAQGAQFAECAEDYBAUFDUAIFAICAIAICBMGCYMQEAEBQEFABAQDYUAIBAUBBUAQBAIEDSAQBAEBDCAQCAICQQ",
        win_rate: 0.5806451612903226,
        play_rate: 0.0535405872193437,
      },
      {
        play_num: 28,
        deck_code:
          "CQCQCAYCCQAQIAQPAECQUOQCAUBAIGQEAEBAQDBMGICACAQCAUAQGAQFAECAPCQBAMAQECZRHEAQCBACA4",
        win_rate: 0.5,
        play_rate: 0.04835924006908463,
      },
    ],
    matchup: [
      {
        _id: "faction_BandleCity_Name faction_Bilgewater_Name Nami Twisted Fate",
        match_num: 40,
        win_num: 17,
        win_rate: 0.425,
      },
      {
        _id: "faction_BandleCity_Name faction_ShadowIsles_Name Senna Veigar",
        match_num: 34,
        win_num: 20,
        win_rate: 0.5882352941176471,
      },
      {
        _id: "faction_Freljord_Name faction_Shurima_Name Lissandra Taliyah",
        match_num: 33,
        win_num: 19,
        win_rate: 0.5757575757575758,
      },
      {
        _id: "faction_Demacia_Name faction_MtTargon_Name Pantheon",
        match_num: 30,
        win_num: 16,
        win_rate: 0.5333333333333333,
      },
    ],
    players: [
      {
        _id: "WYhJY6pw4NIVr_RaBc3dd79Fc0Xf1zsV86n4gVn2Q5WFuyB57xxdAYpqs1QW6aMo3JOoILPXZma-9w",
        count: 40.0,
        win_num: 24,
        win_rate: 0.6,
        riot_id: "Sunekichi#moc",
        server: "asia",
      },
      {
        _id: "f6BLAbIK_iGYNgMBnm2bO_ErDWU4Fhnex3vI2okRM-emy2v0ugqxiUtRH2MAXfVEqqmkvUoYLdYkKQ",
        count: 36.0,
        win_num: 23,
        win_rate: 0.6388888888888888,
        riot_id: "FilipeLC#BR1",
        server: "americas",
      },
      {
        _id: "twaJogwnkHj0WaaAepI1NCz4hEf9_BPJbbNm8Rr96Eic4lhYXBFcBRKEnkwGFTrSWxpHtweXchN0WA",
        count: 32.0,
        win_num: 24,
        win_rate: 0.75,
        riot_id: "Sirturmund#NA1",
        server: "americas",
      },
      {
        _id: "Gi7bmNSPLfLmEMPE4C1opnaKiDy9UgR2k_9JdiUQWPjosbaFv8b25KH3r7kfJ6v5i4e7jPiAi7I1Vg",
        count: 31.0,
        win_num: 23,
        win_rate: 0.7419354838709677,
        riot_id: "Sword of Akasha#jp123",
        server: "asia",
      },
      {
        _id: "8vKNB260YSGP5QYO7KMMCXs9brkIof-i5xPuqtRmPg0UUzomsEeJ5sjUtBeYHWuZbCCOJ39_RdiG0A",
        count: 30.0,
        win_num: 14,
        win_rate: 0.4666666666666667,
        riot_id: "eolant#NZ1",
        server: "americas",
      },
    ],
  },
  {
    _id: "faction_Bilgewater_Name faction_Shurima_Name Pyke Rek'Sai",
    play_num: 528,
    play_rate: 0.0387153541575011,
    win_rate: 0.53125,
    match_num: 520,
    decks: [
      {
        play_num: 71,
        deck_code: "CMBAIBAGAEBQKDYGAQDRGQKEIVFFAAQBAQDAOAQEA4ARMAQBAQDAMAYEA4GRANQ",
        win_rate: 0.5492957746478874,
        play_rate: 0.13653846153846153,
      },
      {
        play_num: 51,
        deck_code: "CMBAKBAGAEBQKBYPBACAOAITCY3ECRCKKAAACAIEAYCA",
        win_rate: 0.39215686274509803,
        play_rate: 0.09807692307692308,
      },
      {
        play_num: 43,
        deck_code: "CMBAIBAGAEBQKDYIAQDQCEYWGZAUISSQAEAQIBQHAIAQIBQCAECAORI",
        win_rate: 0.7209302325581395,
        play_rate: 0.08269230769230769,
      },
      {
        play_num: 29,
        deck_code: "CMBAKBAGAEBAGBIPAYCAOEYWIFCEUUABAMCAOAJFHMAQCBAGA4",
        win_rate: 0.6206896551724138,
        play_rate: 0.05576923076923077,
      },
      {
        play_num: 28,
        deck_code: "CMBAIBAGAEBQKDYHAQDQCEYWIFCEUUACAECAORICAQDAEBYBAECAONQ",
        win_rate: 0.42857142857142855,
        play_rate: 0.05384615384615385,
      },
    ],
    matchup: [
      {
        _id: "faction_BandleCity_Name faction_ShadowIsles_Name Senna Veigar",
        match_num: 34,
        win_num: 26,
        win_rate: 0.7647058823529411,
      },
      {
        _id: "faction_BandleCity_Name faction_Bilgewater_Name Nami Twisted Fate",
        match_num: 29,
        win_num: 13,
        win_rate: 0.4482758620689655,
      },
      {
        _id: "faction_Ionia_Name faction_Shurima_Name Ahri Kennen",
        match_num: 27,
        win_num: 8,
        win_rate: 0.2962962962962963,
      },
      {
        _id: "faction_Ionia_Name faction_Piltover_Name Ahri Lulu",
        match_num: 24,
        win_num: 15,
        win_rate: 0.625,
      },
    ],
    players: [
      {
        _id: "ttpBEdKnm6xjZ6cxvx_OKUkMl17i3mf4SbxyrEznRHGZdzELcUKOFi2XcGDiSmq9NKn9q0cdgl6y0A",
        count: 77.0,
        win_num: 45,
        win_rate: 0.5844155844155844,
        riot_id: "ほろう#5585",
        server: "asia",
      },
      {
        _id: "dksv94LygZsfCaIa3FWZKBZ3bHbL5gJAk-f-lrv32ZVM01sEDkWke4UPUZzceHnDpNT5bfssyM5Gag",
        count: 29.0,
        win_num: 13,
        win_rate: 0.4482758620689655,
        riot_id: "Nimue#2311",
        server: "europe",
      },
      {
        _id: "ddwTiPC4A0rBj0McMz6iUWRiLFDmuujfOU9PEIdi4Omw86Nusx0vpdQaxDLTDO-iWJpDbCNiC9C53w",
        count: 29.0,
        win_num: 18,
        win_rate: 0.6206896551724138,
        riot_id: "Dao#LAS",
        server: "americas",
      },
      {
        _id: "PNKz17GPDPihbVguk9AGaaA_cFYsvHqnEdBRA6S4j1MuTVQMQIr27Qo5n01mybTk1gpYreM_VqUIPQ",
        count: 28.0,
        win_num: 20,
        win_rate: 0.7142857142857143,
        riot_id: "alleyCaesar#2L1R",
        server: "europe",
      },
      {
        _id: "9i2iMs8ni3mmftaepc4gmbp6GixuO_MWc9Akl3fujEzZ6Wfxjzyeujca4YHPIIcJZUpdAlYkFdMq0Q",
        count: 27.0,
        win_num: 15,
        win_rate: 0.5555555555555556,
        riot_id: "Kuako#NA1",
        server: "americas",
      },
    ],
  },
]
