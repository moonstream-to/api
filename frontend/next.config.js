module.exports = {
  reactStrictMode: true,
  target: "serverless",
  trailingSlash: true,
  presets: [require.resolve("next/babel")],
  webpack: (config, { isServer }) => {
    // Fixes npm packages that depend on `fs` module
    if (!isServer) {
      // config.node = { fs: 'empty' };
      config.resolve.fallback.fs = false;
    }

    return config;
  },
};
