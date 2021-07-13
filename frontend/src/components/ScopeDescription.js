
import { jsx } from "@emotion/react";
import { ListItem, UnorderedList } from "@chakra-ui/react";
import { useJournalsScopes } from "../core/hooks";

const ScopeDescription = () => {
  const { scopesCache } = useJournalsScopes();

  if (scopesCache.isLoading) return "";
  const scopes = scopesCache.data;

  return (
    <UnorderedList>
      {scopes?.map((scope, idx) => (
        <ListItem key={`li-scopes-${idx}`} fontSize="sm" my={0}>
          {`${scope.scope} --> ${scope.description}`}
        </ListItem>
      ))}
    </UnorderedList>
  );
};

export default ScopeDescription;
