// import React, { useContext, useState, useEffect } from "react";
// // import http from "axios";
// import { useToast } from "../../hooks";
// import JournalsContext from "./context";
// import UserContext from "../UserProvider/context";
// import { useQuery } from "react-query";
// import { JournalService } from "../../services";

// const JournalsProvider = ({ children }) => {
//   const user = useContext(UserContext);
//   const toast = useToast();

//   const journalsCache = useQuery("journals-list", JournalService.getAll, {
//     enabled: !!user,
//     refetchOnWindowFocus: false,
//     refetchOnMount: false,
//     refetchOnReconnect: false,
//     staleTime: 72000,
//     notifyOnStatusChange: false,
//     // refetchInterval: 1000,
//     onError: (error) => {
//       toast(error, "error");
//     },
//   });

//   const getPublicJournals = async (query) => {
//     const data = await JournalService.getPublicJournals();

//     const newPublicJournals = data.data.journals;

//     return [...newPublicJournals];
//   };

//   const publicJournalsCache = useQuery(["journals-public"], getPublicJournals, {
//     enabled: false,
//     onError: (error) => {
//       toast(error, "error");
//     },
//   });

//   return (
//     <JournalsContext.Provider value={{permissions: currentUserPermissions, publicJournalsCache, journalsCache }}>
//       {children}
//     </JournalsContext.Provider>
//   );
// };

// export default JournalsProvider;
