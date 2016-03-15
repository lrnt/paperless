'use strict';

import path from 'path';
import webpack from 'webpack';

export default {
  entry: [
    './client/index.js'
  ],
  output: {
    path: path.join(__dirname, 'dist'),
    filename: 'bundle.js'
  },
  module: {
    loaders: [
      {
        test: /\.js$/,
        include: [path.resolve(__dirname, 'client')],
        loader: 'babel-loader'
      },
      {
        test: /\.css$/,
        include: [path.resolve(__dirname, 'client')],
        loader: 'style-loader!css-loader'
      },
      {
        test: /\.(png|jpg)$/,
        include: [path.resolve(__dirname, 'client')],
        loader: 'url-loader?limit=8192'
      }
    ]
  }
};
