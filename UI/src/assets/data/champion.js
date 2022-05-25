import sets_en from "../../data/en_us.json"

var champs = []
var champObj = {}

sets_en.forEach((set) => {
  set.forEach((card) => {
    if (card.rarityRef == "Champion" && card.collectible) {
      var code = card.cardCode
      champs.push(code)
      champObj[code] = code
    }
  })
})

export default {
  champions: champs,
  champObj: champObj,
}

export const championCards = {
  champions: champs,
  champObj: champObj,
}

// export default { champions: [
//   "01DE012",
//   "01DE022",
//   "01DE042",
//   "01DE045",
//   "01FR009",
//   "01FR024",
//   "01FR038",
//   "01FR039",
//   "01IO009",
//   "01IO015",
//   "01IO032",
//   "01IO041",
//   "01NX006",
//   "01NX020",
//   "01NX038",
//   "01NX042",
//   "01PZ008",
//   "01PZ036",
//   "01PZ040",
//   "01PZ056",
//   "01SI030",
//   "01SI042",
//   "01SI052",
//   "01SI053",
//   "02BW022",
//   "02BW026",
//   "02BW032",
//   "02BW046",
//   "02BW053",
//   "02DE006",
//   "02FR002",
//   "02IO006",
//   "02NX007",
//   "02PZ008",
//   "02SI008",
//   "03BW004",
//   "03DE011",
//   "03FR006",
//   "03IO002",
//   "03MT009",
//   "03MT054",
//   "03MT055",
//   "03MT056",
//   "03MT058",
//   "03MT087",
//   "03NX007",
//   "03PZ003",
//   "03SI005", // End of Set 3
//   "03MT217", // Aphelios
//   "04DE008", // Start of Set 4
//   "04FR005",
//   "04NX004",
//   "04SH003",
//   "04SH020",
//   "04SH047",
//   "04SH067",
//   "04SH073",
//   "04SI005",
//   "04IO005", // Set 4 Second expansion
//   "04MT008",
//   "04SH039",
//   "04PZ001", // Set 4 Third expansion
//   "04BW005",
//   "04SH019",
//   "04SI055", // Viego
//   "04SH130", // Akshan

//   "05BC041", // Start of Set 5
//   "05BC093",
//   "05BC133",
//   "05BC163",
//   "05BW005",
//   "05NX001",
//   "05PZ006",
//   "05SH014",
//   "05SI009", // End of Set 5 First expansion

//   "05PZ022", // Jayce
// ]}
