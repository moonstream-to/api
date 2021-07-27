import { useQuery, useQueryCache, useMutation } from "react-query";
import { GroupService, UserService } from "../services";
import { useToast, useUser } from ".";
import { queryCacheProps } from "./hookCommon";

const useGroup = (groupId) => {
  const { user } = useUser();
  const cache = useQueryCache();
  const toast = useToast();

  const { data: GroupUsersResponse, isLoading, refetch: getUsers } = useQuery(
    ["group-users", groupId],
    GroupService.getGroupUsers,
    queryCacheProps
  );

  const getInvites = async (key, groupId) => {
    var data;
    data = await GroupService.getInvites(groupId);
    const newInvites = data.data.invites;

    return [...newInvites];
  };

  const invitesQueryCache = useQuery(
    ["group-invites", groupId],
    getInvites,
    queryCacheProps
  );

  const [addExistingUser, addUserStatus] = useMutation(
    GroupService.setGroupUser(groupId),
    {
      onMutate: (newUser) => {
        const NewGroupResponse = cache.getQueryData(["group-users", groupId]);
        const previousGroupResponse = JSON.parse(
          JSON.stringify(NewGroupResponse)
        );
        NewGroupResponse.data.users = [
          ...NewGroupResponse.data.users,
          { email: newUser.email, user_type: newUser.role },
        ];
        cache.setQueryData(["group-users", groupId], {
          ...NewGroupResponse,
        });

        return previousGroupResponse;
      },
      onError: (error, variables, context) => {
        cache.setQueryData(["group-users", groupId], context);
        toast(error, "error");
      },

      //fetch data from backend again to fill missing fields of newly added
      //user
      onSuccess: () => {
        getUsers();
      },
    }
  );

  const [sendInvite, sendInviteStatus] = useMutation(
    GroupService.sendInvite(groupId),
    {
      onSuccess: () => {
        invitesQueryCache.refetch();
      },
      onError: (error) => {
        toast(error, "error");
      },
    }
  );

  /**
   * addToGroup adds to group.
   *
   * If `email` is specified and found our users DB - add user.
   *
   * If `email` is specified and not found in users DB - send invite link
   *
   * If `email` not specified - return public invite code
   */
  const addToGroup = async (invitee) => {
    if (invitee?.email) {
      const query = `email=${invitee.email}`;

      await UserService.findUser(query).then(
        (response) => {
          if (response.data.user_id) {
            addExistingUser(invitee);
          }
        },
        () => {
          if (invitee.email) {
            sendInvite(invitee);
          } else {
            toast("user not found", "error");
          }
        }
      );
    } else {
      sendInvite();
    }
  };

  //ToDo: const addUserMutation = useMutation(.. when upgrading to React Query 3
  const addUserMutation = {
    addUser: addToGroup,
    isLoading: addUserStatus.isLoading,
  };

  const [removeUser, removeUserStatus] = useMutation(
    GroupService.deleteGroupUser(groupId),
    {
      onMutate: (removedUsername) => {
        const NewGroupResponse = cache.getQueryData(["group-users", groupId]);
        const previousGroupResponse = JSON.parse(
          JSON.stringify(NewGroupResponse)
        );
        NewGroupResponse.data.users = NewGroupResponse.data.users.filter(
          (user) => user.username !== removedUsername
        );
        cache.setQueryData(["group-users", groupId], {
          ...NewGroupResponse,
        });
        if (user.username === removedUsername) {
          const NewGroupsResponse = cache.getQueryData(["groups"]);
          const previousGroupsResponse = JSON.parse(
            JSON.stringify(NewGroupsResponse)
          );
          NewGroupsResponse.data[groupId].user_type = "none";

          cache.setQueryData(["groups"], {
            ...NewGroupsResponse,
          });

          return { previousGroupResponse, previousGroupsResponse };
        } else {
          return { previousGroupResponse };
        }
      },
      onError: (error, variables, context) => {
        cache.setQueryData(
          ["group-users", groupId],
          context.previousGroupResponse
        );
        if (context.previousGroupsResponse) {
          cache.setQueryData(["groups"], context.previousGroupsResponse);
        }

        toast(error, "error");
      },

      onSuccess: (response, username) => {
        if (user.username === username) {
          const NewGroupsResponse = cache.getQueryData(["groups"]);
          delete NewGroupsResponse.data[groupId];

          cache.setQueryData(["groups"], {
            ...NewGroupsResponse,
          });
        }
      },
    }
  );

  //ToDo: const removeUserMutation = useMutation(.. when upgrading to React Query 3
  const removeUserMutation = {
    removeUser,
    isLoading: removeUserStatus.isLoading,
  };

  const [revokeInvite, activatePublicInviteStatus] = useMutation(
    GroupService.deleteInvite(groupId),
    {
      onSuccess: () => {
        invitesQueryCache.refetch();
      },
    }
  );

  const users = {
    isLoading: isLoading,
    data: GroupUsersResponse?.data?.users,
    refetch: getUsers,
  };

  const readInvites = ({ isPublic, isPersonal }) => {
    const allInvites = cache.getQueryData(["group-invites", groupId]);
    if (allInvites) {
      if (isPublic && isPersonal) {
        return allInvites;
      } else if (isPersonal) {
        return allInvites.filter((item) => item.email && item.active);
      } else {
        return allInvites.filter((item) => !item.email && item.active);
      }
    }
  };

  const invites = {
    personal: readInvites({ isPublic: false, isPersonal: true }),
    public: readInvites({ isPublic: true, isPersonal: false }),
    all: readInvites({ isPublic: true, isPersonal: true }),
    isLoading: invitesQueryCache.isLoading,
    get: () => invitesQueryCache.refetch(),

    createPersonal: addToGroup,
    createPublic: () => addToGroup(),
    isLoadingCreate: sendInviteStatus.isLoading,
    revokeInvite: revokeInvite,
    isLoadingRevoke: activatePublicInviteStatus.isLoading,
  };

  return {
    users,
    addUserMutation,
    removeUserMutation,
    invites,
  };
};

export default useGroup;
