/**
 * Main file of webpack config for RTL.
 * Please do not modify unless you know what to do
 */
const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const del = require("del");
const RtlCssPlugin = require("rtlcss-webpack-plugin");

// global variables
const rootPath = path.resolve(__dirname);
const distPath = rootPath + "/src/assets";

const entries = {
  "css/style": "./src/assets/sass/style.scss",
};

// remove older folders and files
(async () => {
  await del.sync(distPath + "/css", { force: true });
})();

function mainConfig() {
  return {
    // enabled/disable optimizations
    mode: "development",
    // console logs output, https://webpack.js.org/configuration/stats/
    stats: "errors-only",
    performance: {
      // disable warnings hint
      hints: false,
    },
    entry: entries,
    output: {
      // main output path in assets folder
      path: distPath,
      // output path based on the entries' filename
      filename: "[name].js",
    },
    resolve: {
      extensions: [".scss"],
    },
    plugins: [
      new MiniCssExtractPlugin({
        filename: "[name].css",
      }),
      new RtlCssPlugin({
        filename: "[name].rtl.css",
      }),
      {
        apply: (compiler) => {
          // hook name
          compiler.hooks.afterEmit.tap("AfterEmitPlugin", () => {
            (async () => {
              await del.sync(distPath + "/css/*.js", { force: true });
            })();
          });
        },
      },
    ],
    module: {
      rules: [
        {
          test: /\.scss$/,
          use: [
            MiniCssExtractPlugin.loader,
            "css-loader",
            {
              loader: "sass-loader",
              options: {
                sourceMap: true,
              },
            },
          ],
        },
      ],
    },
  };
}

module.exports = function () {
  return [mainConfig()];
};
