export const PERMISSION_LEVELS = { none: 0, member: 1, admin: 10, owner: 100 };

export const PRESIGNED_URL_TYPE = {
  SESSIONS: "session",
  CLIENTS: "client",
  REPORTS: "stats",
  ERRORS: "errors",
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

export const PRESERVE_QUERY_ACROSS_JOURNALS = false;
export const PRICING_OPTIONS = { DEV: 1, NIGHTLY: 2, STABLE: 3 };

const constants = { PERMISSION_LEVELS, PRESIGNED_URL_TYPE, DEFAULT_METATAGS };

export default constants;
