import { useQuery, useMutation, useQueryClient } from "react-query";
import { JournalService } from "../services";
import { useToast } from ".";
import { queryCacheProps } from "./hookCommon";

const useJournalPermissions = (journalId, journalScope) => {
  const cache = useQueryClient();
  const toast = useToast();
  const {
    data,
    isLoading,
    refetch: getPermissions,
    error,
  } = useQuery(
    ["journal-permissions", { journalId }],
    async () => {
      if (journalId) {
        if (journalScope === "personal") {
          const response = await JournalService.getJournalPermissions(
            journalId
          );
          if (!response.data || !response.data.permissions) {
            return [];
          }
          return response.data.permissions;
        } else {
          return [];
        }
      } else {
        const response = { data: { scopes: ["public"] } };
        return response;
      }
    },
    queryCacheProps
  );

  const {
    data: currentUserPermissions,
    refetch: getCurrentUserPermissions,
    isLoading: currentUserPermissionsIsLoading,
  } = useQuery(
    ["journal-permissions-current-user", { journalId }],
    async () => {
      if (journalId) {
        if (journalScope === "personal") {
          let response = { data: {} };
          try {
            response = await JournalService.getCurrentUserJournalPermissions(
              journalId
            );
          } catch (error) {
            console.warn("error retrieving scopes:", error);
          }
          if (!response.data || !response.data.scopes) {
            return [];
          }
          return response.data.scopes.map((scope) => scope.permission);
        } else {
          return [];
        }
      } else {
        const response = { data: { scopes: ["public"] } };
        return response;
      }
    },
    {
      ...queryCacheProps,
      staleTime: 720000, // 12 hours
    }
  );

  const setJournalPermissionMutation = useMutation(
    JournalService.setJournalPermission(journalId),
    {
      onMutate: (data) => {
        const newJournalPermissionResponse = cache.getQueryData([
          "journal-permissions",
          { journalId },
        ]);
        const previousJournalPermissionResponse = JSON.parse(
          JSON.stringify(newJournalPermissionResponse)
        );
        const index = previousJournalPermissionResponse.findIndex(
          (i) => i.holder_id === data.holder_id
        );

        if (index === -1) {
          newJournalPermissionResponse.push({
            permissions: [...data.permission_list],
            holder_id: data.holder_id,
            holder_type: data.holder_type,
          });
        } else {
          newJournalPermissionResponse[index].permissions = [
            ...newJournalPermissionResponse[index].permissions,
            ...data.permission_list,
          ];
        }

        cache.setQueryData(
          ["journal-permissions", { journalId }],
          newJournalPermissionResponse
        );

        return previousJournalPermissionResponse;
      },
      onError: (error, value, context) => {
        cache.setQueryData(["journal-permissions", { journalId }], context);

        toast(error, "error");
      },

      onSuccess: () => {
        getCurrentUserPermissions();
      },
    }
  );

  const removeJournalPermissionMutation = useMutation(
    JournalService.deleteJournalPermission(journalId),
    {
      onMutate: (data) => {
        const newJournalPermissionResponse = cache.getQueryData([
          "journal-permissions",
          { journalId },
        ]);
        const previousJournalPermissionResponse = JSON.parse(
          JSON.stringify(newJournalPermissionResponse)
        );
        const index = previousJournalPermissionResponse.findIndex(
          (i) => i.holder_id === data.holder_id
        );
        newJournalPermissionResponse[index].permissions =
          newJournalPermissionResponse[index].permissions.filter(
            (value) => !data.permission_list.includes(value)
          );

        if (newJournalPermissionResponse[index].permissions.length < 1) {
          newJournalPermissionResponse.splice(index, 1);
        }

        cache.setQueryData(
          ["journal-permissions", { journalId }],
          newJournalPermissionResponse
        );

        return previousJournalPermissionResponse;
      },
      onError: (error, value, context) => {
        cache.setQueryData(["journal-permissions", { journalId }], context);

        toast(error, "error");
      },

      onSuccess: () => {
        getCurrentUserPermissions();
      },
    }
  );

  const holders = data;
  return {
    holders,
    isLoading,
    getPermissions,
    error,
    setJournalPermissionMutation,
    removeJournalPermissionMutation,
    currentUserPermissions,
    currentUserPermissionsIsLoading,
  };
};

export default useJournalPermissions;
