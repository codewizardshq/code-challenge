module.exports = {
  "lintOnSave": false,
  "transpileDependencies": [
    "vuetify"
  ],
  "outputDir": "dist",
  "devServer": {
    "disableHostCheck": true,
    "proxy": {
      "/api/*": {
        "target": "http://localhost:5000/"
      },
      "/assets/*": {
        "target": "http://localhost:5000/"
      }
    }
  }
}