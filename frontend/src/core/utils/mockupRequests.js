import moment from "moment";
const MOCK_API = process.env.NEXT_PUBLIC_SIMIOTICS_AUTH_URL;
var MockAdapter = require("axios-mock-adapter");
const makeid = (length) => {
  var result = "";
  var characters =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  var charactersLength = characters.length;
  for (var i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
};

const randDate = () => {
  return moment(
    new Date(+new Date() - Math.floor(Math.random() * 10000000000))
  ).format("MM/DD/YYYY");
};
let MockSubscriptions = [
  {
    address: makeid(24),
    id: makeid(24),
    notes: "lorem", //ToDo: rename in to label
    created_at: randDate(),
    subscription_type: "ethereum_blockchain",
  },
  {
    address: makeid(24),
    id: makeid(24),
    notes: "lorem",
    created_at: randDate(),
    subscription_type: "ethereum_txpool",
  },
  {
    address: makeid(24),
    id: makeid(24),
    notes: "lorem",
    created_at: randDate(),
    subscription_type: "algorand_blockchain",
  },
  {
    address: makeid(24),
    id: makeid(24),
    notes: "lorem",
    created_at: randDate(),
    subscription_type: "ethereum_blockchain",
  },
  {
    address: makeid(24),
    id: makeid(24),
    notes: "lorem",
    created_at: randDate(),
    subscription_type: "ethereum_blockchain",
  },
];
const enableMockupRequests = (axiosInstance) => {
  let mock = new MockAdapter(axiosInstance, { onNoMatch: "passthrough" });

  mock.onGet(`${MOCK_API}/subscription_types/`).reply(200, {
    data: [
      {
        subscription_type: "ethereum_blockchain",
        id: makeid(24),
        name: "Ethereum",
        active: true,
        subscription_plan_id: makeid(24),
      },
      {
        subscription_type: "ethereum_txpool",
        id: makeid(24),
        name: "Ethereum Transaction Pool",
        active: true,
        subscription_plan_id: makeid(24),
      },
      {
        subscription_type: "algorand_blockchain",
        id: makeid(24),
        name: "Algorand",
        active: false,
        subscription_plan_id: makeid(24),
      },
      {
        subscription_type: "free",
        id: makeid(24),
        name: "Free subscription",
        active: true,
        subscription_plan_id: null,
      },
    ],
  });

  mock.onGet(`${MOCK_API}/subscriptions/`).reply(200, {
    data: {
      is_free_subscription_availible: true,
      subscriptions: MockSubscriptions,
    },
  });

  mock.onPost(`${MOCK_API}/subscriptions/`).reply((config) => {
    const params = config.data; // FormData of {name: ..., file: ...}
    const id = params.get("id");
    const note = params.get("note");

    return new Promise(function (resolve) {
      setTimeout(function () {
        const data = { id, note };
        console.log("mock", id, note);
        MockSubscriptions.push({ ...data });
        resolve([200, { message: "OK", result: true }]);
      }, 1000);
    });
  });
};
export default enableMockupRequests;
