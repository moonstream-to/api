import { v4 as uuid4 } from "uuid";

const KEY_BUGOUT_CLIENT_ID = "BUGOUT_CLIENT_ID";

const useClientID = () => {
  // const location = useLocation();
  // const query = new URLSearchParams(location.search);
  let clientID = localStorage.getItem(KEY_BUGOUT_CLIENT_ID);

  // const queryParametersClientID = query.get("clientID");
  // if (queryParametersClientID && queryParametersClientID !== clientID) {
  //   clientID = queryParametersClientID;
  //   localStorage.setItem(KEY_BUGOUT_CLIENT_ID, clientID);
  // }

  if (!clientID) {
    const newClientID = uuid4();
    clientID = newClientID;
    localStorage.setItem(KEY_BUGOUT_CLIENT_ID, newClientID);
  }

  return clientID;
};

export default useClientID;
