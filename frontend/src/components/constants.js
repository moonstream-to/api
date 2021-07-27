export const PERMISSION_LEVELS = { none: 0, member: 1, admin: 10, owner: 100 };

export const PRESIGNED_URL_TYPE = {
  SESSIONS: "session",
  CLIENTS: "client",
  REPORTS: "stats",
  ERRORS: "errors",
};

export const DEFAULT_METATAGS = {
  title: "Bugout: Measure the success of your dev tool",
  description:
    "Get usage metrics and crash reports. Improve your users' experience",
  keywords:
    "bugout, bugout-dev, bugout.dev, usage-metrics, analytics, dev-tool ,knowledge, docs, journal, entry, find-anything",
  url: "https://bugout.dev",
  image: "https://s3.amazonaws.com/static.simiotics.com/landing/aviator-2.svg",
};

export const PRESERVE_QUERY_ACROSS_JOURNALS = false;
export const PRICING_OPTIONS = { DEV: 1, NIGHTLY: 2, STABLE: 3 };

const constants = { PERMISSION_LEVELS, PRESIGNED_URL_TYPE, DEFAULT_METATAGS };

export default constants;
