const { merge } = require('webpack-merge');
const commonConfig = require('./common.config');

module.exports = merge(commonConfig, {
  mode: 'development',
  devtool: 'inline-source-map',
  devServer: {
    port: 3000,
    // devtool: 'inline-source-map',

    proxy: {
      {%- if cookiecutter.use_docker == 'n' %}
      '/': 'http://0.0.0.0:8000',
      {%- else %}
      '/': 'http://django:8000',
      {%- endif %}
    },
    watchFiles: ['{{ cookiecutter.project_slug }}/templates'],
    // hot: false,
    // liveReload: true,
  },
})
