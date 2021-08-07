import { useInfiniteQuery } from "react-query";
import { queryCacheProps } from "./hookCommon";
import { SubscriptionsService } from "../services";
import moment from "moment";

// const useJournalEntries = ({
//   refreshRate,
//   isContent,
//   pageSize,
//   searchQuery,
//   enabled,
// }) => {
//   //const limit = pageSize ? pageSize : 25;

//   const getStream =
//     (searchTerm) =>
//     async ({
//       pageParam = {
//         start_time: moment().unix(),
//       },
//     }) => {
//       console.log("pageParam", pageParam);
//       console.log("moment().unix()", moment().unix());

//       const response = await SubscriptionsService.getStream({
//         searchTerm: searchTerm,
//         start_time: pageParam.start_time,
//         end_time: pageParam.start_time - 1000,
//       });

//       const newEntryList = response.data.stream.map((entry) => ({
//         ...entry,
//       }));

//       console.log("response.data", response.data);
//       return {
//         data: [...newEntryList],
//         pageParams: {
//           next_future_timestamp: response.data.next_future_timestamp,
//           next_past_transaction_timestamp:
//             response.data.next_past_transaction_timestamp,
//           start_time: response.data.start_time,
//           end_time: response.data.end_time,
//         },
//       };
//     };

//   const {
//     data: EntriesPages,
//     isFetchingMore,
//     isLoading,
//     hasPreviousPage,
//     fetchPreviousPage,
//     hasNextPage,
//     fetchNextPage,
//     refetch,
//   } = useInfiniteQuery(["stream", { searchQuery }], getStream(searchQuery), {
//     refetchInterval: refreshRate,
//     ...queryCacheProps,
//     getNextPageParam: (lastGroup) => {
//       return {
//         start_time: moment().unix(),
//       };
//     },
//     getPreviousPageParam: (lastGroup) => {
//       return {
//         start_time: lastGroup.pageParams.next_past_transaction_timestamp,
//       };
//     },
//     onSuccess: () => {},
//     enabled: !!enabled,
//   });

//   return {
//     EntriesPages,
//     hasPreviousPage,
//     fetchPreviousPage,
//     hasNextPage,
//     fetchNextPage,
//     isFetchingMore,
//     refetch,
//     isLoading,
//   };
// };

const useJournalEntries = ({
  refreshRate,
  searchQuery,
  start_time,
  end_time,
  include_start,
  include_end,
  enabled,
}) => {
  // set our get method
  const getStream =
    (searchTerm, start_time, end_time, include_start, include_end) =>
    async () => {

      // Request with params to streams
      const response = await SubscriptionsService.getStream({
        searchTerm: searchTerm,
        start_time: start_time,
        end_time: end_time,
        include_start: include_start,
        include_end: include_end,
      });

      // new events from stream
      const newEventsList = response.data.stream.map((event) => ({
        ...event,
      }));

      return {
        data: [...newEventsList],
        pageParams: {
          // timeinterval
          start_time: response.data.start_time, // from old
          end_time: response.data.end_time, // to new

          // closes available transactions
          next_event_time: response.data.next_event_time,
          previous_event_time: response.data.previous_event_time,

          // boundaries
          include_start: response.data.include_start,
          include_end: response.data.include_end,
        },
      };
    };


    const {

        data,
        isLoading, 
        refetch,

        } = useQuery(["stream", { searchQuery }], getStream(searchQuery, 
                                                            start_time,
                                                            end_time,
                                                            include_start,
                                                            include_end ),
        {
          refetchInterval: refreshRate,
          ...queryCacheProps,
          onSuccess: () => {},
          enabled: !!enabled,
        });
      
        return {
        EntriesPages: data,
        isLoading, 
        refetch,
        };
      };
};
export default useJournalEntries;
