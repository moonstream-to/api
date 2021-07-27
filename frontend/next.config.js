module.exports = {
  reactStrictMode: true,
  target: "serverless",
  trailingSlash: true,
  presets: [
    require.resolve('next/babel')
  ]
};