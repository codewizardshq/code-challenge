module.exports = {
  lintOnSave: false,
  transpileDependencies: ["vuetify"],
  outputDir: "dist",
  css: {
    extract: { ignoreOrder: true },
  },
  devServer: {
    disableHostCheck: true,
    proxy: {
      "/api/*": {
        // Forward frontend dev server request for /api to flask dev server
        target: "http://localhost:5000/"
      },
      "/assets/*": {
        // Forward frontend dev server request for /api to flask dev server
        target: "http://localhost:5000/"
      }
    }
  }
};
