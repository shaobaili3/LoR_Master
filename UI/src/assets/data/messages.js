import en from "./i18n/en.json"
import jp from "./i18n/ja-JP.json"
import zhT from "./i18n/zh-TW.json"
import zhC from "./i18n/zh-CN.json"
import pt from "./i18n/pt-BR.json"
import deu from "./i18n/de-DE.json"

export default {
  English: en,
  繁體中文: zhT,
  简体中文: zhC,
  "Português (Brasil)": pt,
  日本語: jp,
  Deutsch: deu
}

import { zhCN, zhTW, ja, enUS, ptBR, de } from "date-fns/locale"

export const dateFNSLocales = {
  English: enUS,
  繁體中文: zhCN,
  简体中文: zhTW,
  "Português (Brasil)": ptBR,
  日本語: ja,
  Deutsch: de
}
