module.exports = {
  publicPath: process.env.NODE_ENV === "production" ? "" : "/",
  pages: {
    index: {
      // entry for the page
      entry: "src/pages/home/main.js",
      // the source template
      template: "public/index.html",
      // output as dist/index.html
      filename: "index.html",
      // when using title option,
      // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
      title: "MaRu Tracker App",
      // chunks to include on this page, by default includes
      // extracted common chunks and vendor chunks.
      // chunks: ['chunk-vendors', 'chunk-common', 'index']
    },
    info: {
      entry: "src/pages/info/main.js",
      template: "public/index.html",
      filename: "info.html",
      title: "MaRu Tracker Info",
    },
    deck: {
      entry: "src/pages/deck/main.js",
      template: "public/index.html",
      filename: "deck.html",
      title: "MaRu Tracker Deck",
    },
  },
  // chainWebpack: config => {
  //   config
  //       .plugin('html')
  //       .tap(args => {
  //           args[0].title = "MaRu Tracker UI";
  //           return args;
  //       })
  // }
}
