const path = require('path')
const BundleTracker = require('webpack-bundle-tracker')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const devMode = process.env.NODE_ENV !== 'production'

module.exports = {
  target: 'web',
  context: path.join(__dirname, '../'),
  entry: {
    base: path.resolve(
      __dirname,
      '../{{cookiecutter.project_slug}}/static/js/base'
    ),
  },
  output: {
    path: path.resolve(
      __dirname,
      '../{{cookiecutter.project_slug}}/static/webpack_bundles/'
    ),
    publicPath: '/static/webpack_bundles/',
    filename: 'js/[name]-[fullhash].js',
    chunkFilename: 'js/[name]-[hash].js',
  },
  plugins: [
    new BundleTracker({
      filename: path.resolve(__dirname, '../webpack-stats.json'),
    }),
    new MiniCssExtractPlugin({
      filename: devMode ? 'css/[name].css' : 'css/[name].[contenthash].css',
    }),
  ],
  module: {
    rules: [
      // we pass the output from babel loader to react-hot loader
      {
        test: /\.js$/,
        loader: 'babel-loader',
      },
      {
        test: /\.s?css$/i,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          {
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                plugins: ['postcss-preset-env', 'autoprefixer', 'pixrem'],
              },
            },
          },
          'sass-loader',
        ],
      },
    ],
  },

  resolve: {
    modules: ['node_modules'],
    extensions: ['.js', '.jsx'],
  },

  optimization: {
    runtimeChunk: 'single',

    splitChunks: {
      cacheGroups: {
        commons: {
          name: 'common',
          chunks: 'all',
          minChunks: 2,
          reuseExistingChunk: true,
        },
      },
    },
  },
}
