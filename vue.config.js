module.exports = {
  "lintOnSave": false,
  "transpileDependencies": [
    "vuetify"
  ],
  outputDir: 'dist',
  devServer: {
    proxy: {
      '/api*': {
        // Forward frontend dev server request for /api to flask dev server
        target: 'http://localhost:5000/'
      }
    }
  }
}
