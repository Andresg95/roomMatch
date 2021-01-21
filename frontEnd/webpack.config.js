var HtmlWebpackPlugin = require("html-webpack-plugin");
var path = require("path");
var basePath = __dirname;

module.exports = {
    context: path.join(basePath, "src"),
    resolve: {
        extensions: [".js", ".jsx"],
    },
    entry: ["./index.jsx", "react", "react-dom"],

    output: {
        filename: "bundle.js",
        publicPath: "/",
    },

    module: {
        rules: [{
                test: /\.jsx?$/,
                exclude: /node_modules/,
                loader: "babel-loader",
            },
            {
                test: /\.scss$/,
                use: [
                    "style-loader",
                    "css-loader",
                    {
                        loader: "sass-loader",
                        options: {
                            implementation: require("sass"),
                        },
                    },
                ],
            },
            {
                test: /\.css$/,
                exclude: /node_modules/,
                use: [{
                        loader: "style-loader",
                    },
                    {
                        loader: "css-loader",
                    },
                ],
            },
            {
                test: /\.(png|jpg)$/,
                exclude: /node_modules/,
                loader: "url-loader?limit=5000",
            },
            {
                test: /\.html$/,
                loader: "html-loader",
            },
        ],
    },

    plugins: [
        new HtmlWebpackPlugin({
            filename: "index.html", //Name of file in ./dist/
            template: "index.html", //Name of template in ./src
            hash: true,
        }),
    ],

    devServer: {
        port: 8080,
        historyApiFallback: true,

        proxy: {
            "/api": "http://localhost:5000",
        },
    },
};