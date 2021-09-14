export const MOONSTREAM_API_URL = process.env.NEXT_PUBLIC_MOONSTREAM_API_URL;

export const BUGOUT_ENDPOINTS = {
  Usage: "usage",
  Web: "parasite",
};

export const DEFAULT_METATAGS = {
  title: "Moonstream.to: All your crypto data in one stream",
  description:
    "From the Ethereum transaction pool to Elon Musk’s latest tweets get all the crypto data you care about in one stream.",
  keywords:
    "blockchain, crypto, data, trading, smart contracts, ethereum, solana, transactions, defi, finance, decentralized",
  url: "https://www.moonstream.to",
  image: `https://s3.amazonaws.com/static.simiotics.com/moonstream/assets/crypto+traders.png`,
};

export const ALL_NAV_PATHES = [
  {
    title: "Product",
    path: "/product",
  },
  {
    title: "Team",
    path: "/team",
  },
];

export const USER_NAV_PATHES = [
  {
    title: "Learn how to use Moonstream",
    path: "/welcome",
  },
];

export const PAGE_SIZE = 10;

export const AWS_ASSETS_PATH = `https://s3.amazonaws.com/static.simiotics.com/moonstream/assets`;
export const WHITE_LOGO_W_TEXT_URL = `https://s3.amazonaws.com/static.simiotics.com/moonstream/assets/moon-logo%2Btext-white.svg`;
