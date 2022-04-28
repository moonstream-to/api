export const MOONSTREAM_API_URL = process.env.NEXT_PUBLIC_MOONSTREAM_API_URL;

export const BUGOUT_ENDPOINTS = {
  Usage: "usage",
  Web: "parasite",
};

export const DEFAULT_METATAGS = {
  title: "Moonstream: Building blocks for your blockchain economy",
  description:
    "Moonstream DAO makes tools that help you build, manage, and secure your blockchain economy.",
  keywords:
    "analytics, blockchain analytics, protocol, protocols, blockchain, crypto, data, NFT gaming, smart contracts, web3, smart contract, ethereum, polygon, matic, transactions, defi, finance, decentralized, mempool, NFT, NFTs, DAO, DAOs, cryptocurrency, cryptocurrencies, bitcoin, blockchain economy, marketplace, blockchain security, loyalty program, Ethereum bridge, Ethereum bridges, NFT game, NFT games",
  url: "https://www.moonstream.to",
  image: `https://s3.amazonaws.com/static.simiotics.com/moonstream/assets/crypto+traders.png`,
};

// export const FOOTER_COLUMNS = {
//   NEWS: "News",
//   COMPANY: "Company",
//   PRODUCT: "Product",
// };

export const SIITEMAP_CATEGORIES = {
  SOLUTIONS: "Solutions",
  DEVELOPERS: "Developers",
  RESOURCES: "Resources",
  ABOUT: "About",
};

export const PAGETYPE = {
  EMPTY: 0,
  CONTENT: 1,
  EXTERNAL: 2,
};

export const SITEMAP = [
  {
    title: "Resources",
    path: "/resources",
    type: PAGETYPE.EMPTY,
    children: [
      {
        title: "Case studies",
        path: "https://docs.google.com/document/d/1mjfF8SgRrAZvtCVVxB2qNSUcbbmrH6dTEYSMfHKdEgc",
        type: PAGETYPE.EXTERNAL,
      },
      {
        title: "Whitepapers",
        path: "/whitepapers",
        type: PAGETYPE.CONTENT,
      },
      {
        title: "Blog",
        path: "https://blog.moonstream.to",
        type: PAGETYPE.EXTERNAL,
      },
    ],
  },
  {
    title: "Developers",
    path: "/developers",
    type: PAGETYPE.EMPTY,

    children: [
      {
        title: "Docs",
        path: "/docs",
        type: PAGETYPE.CONTENT,
      },
      {
        title: "Status",
        path: "/status",
        type: PAGETYPE.CONTENT,
      },
    ],
  },

  {
    title: "About",
    path: "/about",
    type: PAGETYPE.EMPTY,
    children: [
      {
        title: "Team",
        path: "/team",
        type: PAGETYPE.CONTENT,
      },
    ],
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
export const WHITE_LOGO_W_TEXT_URL = `https://s3.amazonaws.com/static.simiotics.com/moonstream/assets/moon-logo%2Btext-white.png`;

export const TIME_RANGE_SECONDS = {
  day: 86400,
  week: 86400 * 7,
  month: 86400 * 28,
};

export const CHART_METRICS = {
  GENERIC: "genetic",
  FUNCTIONS: "function",
  EVENTS: "event",
};

export const DASHBOARD_UPDATE_ACTIONS = {
  RENAME_DASHBOARD: 0,
  APPEND_METRIC: 1,
  DROP_METRIC: 2,
  APPEND_SUBSCRIPTION: 4,
  DROP_SUBSCRIPTION: 6,
  OVERRIDE_DASHBOARD: 7,
  OVERRIDE_SUBSCRIPTION: 8,
  RESET_TO_DEFAULT: 9,
};

export const DASHBOARD_CONFIGURE_SETTING_SCOPES = {
  METRICS_ARRAY: 1, //Scope to change whole array (methods | events | generics)
  METRIC_NAME: 2, //Scope to one metric based on name
  METRICS_ALL: 3, //Scope to replace whole subscription_setting object keeping subscriptionId
};

export const GENERIC_METRICS = [
  "transactions_in",
  "transactions_out",
  "value_in",
  "value_out",
  "balance",
];
