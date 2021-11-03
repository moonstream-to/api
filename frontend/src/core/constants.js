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

export const FOOTER_COLUMNS = {
  NEWS: "News",
  COMPANY: "Company",
  PRODUCT: "Product",
};

export const ALL_NAV_PATHES = [
  {
    title: "Product",
    path: "/product",
    footerCategory: FOOTER_COLUMNS.PRODUCT,
  },
  {
    title: "Team",
    path: "/team",
    footerCategory: FOOTER_COLUMNS.COMPANY,
  },
  {
    title: "API",
    path: "https://api.moonstream.to/docs",
    footerCategory: FOOTER_COLUMNS.PRODUCT,
  },
  {
    title: "Whitepapers",
    path: "/whitepapers",
    footerCategory: FOOTER_COLUMNS.PRODUCT,
  },
  {
    title: "Blog",
    path: "https://blog.moonstream.to",
    footerCategory: FOOTER_COLUMNS.NEWS,
  },
];

export const USER_NAV_PATHES = [
  {
    title: "Learn how to use Moonstream",
    path: "/welcome",
  },
];

export const PAGE_SIZE = 20;

export const AWS_ASSETS_PATH = `https://s3.amazonaws.com/static.simiotics.com/moonstream/assets`;
export const WHITE_LOGO_W_TEXT_URL = `https://s3.amazonaws.com/static.simiotics.com/moonstream/assets/moon-logo%2Btext-white.svg`;

export const TIME_RANGE_SECONDS = {
  day: 86400,
  week: 86400 * 7,
  month: 86400 * 28,
};
