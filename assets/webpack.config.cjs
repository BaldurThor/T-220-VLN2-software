const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const path = require('path')
module.exports = {
    entry: './index.js',
    mode: 'development',
    module: {
        rules: [
            {
                test: /\.s[ac]ss$/i,
                use: [
                    MiniCssExtractPlugin.loader,
                    "css-loader",
                    "sass-loader",
                ],
            },
            {
                test: /\.(woff|woff2|eot|ttf|otf)$/i,
                type: "asset/inline",
            },
        ]
    },
    plugins: [].concat([new MiniCssExtractPlugin()]),
};