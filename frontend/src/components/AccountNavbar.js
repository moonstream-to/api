import React from "react";
import { useUser, useRouter } from "../core/hooks";
import { useEffect, Fragment, useState } from "react";
import { Heading, Center, Spinner, Link, Button } from "@chakra-ui/react";
import RouterLink from "next/link";
const ACCOUNT_SCREEN_WIDGETS = {
  tokens: "tokens",
  security: "security",
  teams: "teams",
};

const AccountNavbar = () => {
  const router = useRouter();
  const [CurrentWidget, setCurrentWidget] = useState();
  const { user, isInit } = useUser();

  useEffect(() => {
    if (isInit) {
      if (user) {
        if (router.pathname === "/account") {
          router.replace("/account/teams");
        }
      } else {
        router.replace("/register");
      }
    }
  }, [router, CurrentWidget, user, isInit]);

  useEffect(() => {
    setCurrentWidget(router.nextRouter.query.page);
  }, [setCurrentWidget, router.nextRouter.query.page]);

  if (!user && !isInit)
    return (
      <Center>
        <Spinner
          hidden={false}
          my={32}
          size="lg"
          color="primary.500"
          thickness="4px"
          speed="1.5s"
        />
      </Center>
    );

  return (
    <Fragment>
      <Center>
        <Heading as="h1" fontSize={["md", "lg"]} py={4} color="black.100">
          My Account
        </Heading>
      </Center>

      <Link
        as={RouterLink}
        href={`/account/${ACCOUNT_SCREEN_WIDGETS.teams}`}
        passHref
      >
        <Button
          isActive={CurrentWidget === ACCOUNT_SCREEN_WIDGETS.teams}
          // ref={TeamsButtonRef}
          //   href={`/account/${ACCOUNT_SCREEN_WIDGETS.teams}`}
          variant="accountMenu"
          colorScheme="secondary"
          as={Link}
        >
          Teams
        </Button>
      </Link>
      <Link
        as={RouterLink}
        href={`/account/${encodeURIComponent(ACCOUNT_SCREEN_WIDGETS.tokens)}`}
        passHref
      >
        <Button
          as={Link}
          isActive={CurrentWidget === ACCOUNT_SCREEN_WIDGETS.tokens}
          // ref={TokensButtonRef}
          colorScheme="secondary"
          variant="accountMenu"
        >
          Tokens
        </Button>
      </Link>
      <Link
        as={RouterLink}
        href={`/account/${ACCOUNT_SCREEN_WIDGETS.security}`}
        passHref
      >
        <Button
          isActive={CurrentWidget === ACCOUNT_SCREEN_WIDGETS.security}
          as={Link}
          // ref={SecurityButtonRef}
          // as={RouterLink}
          // href={`/account/${ACCOUNT_SCREEN_WIDGETS.security}`}
          variant="accountMenu"
          colorScheme="secondary"
        >
          Security
        </Button>
      </Link>
    </Fragment>
  );
};

export default AccountNavbar;
