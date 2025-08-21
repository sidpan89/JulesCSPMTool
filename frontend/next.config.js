/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // This is to allow Docker to work with Next.js's file watching in development
  webpackDevMiddleware: config => {
    config.watchOptions = {
      poll: 1000,
      aggregateTimeout: 300,
    }
    return config
  },
};

module.exports = nextConfig;
