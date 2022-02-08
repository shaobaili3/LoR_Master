export default {
  target: "electron-renderer",
  output: {
    publicPath: argv.mode === "production" ? "/" : "/",
  },
}
