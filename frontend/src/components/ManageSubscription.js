
import { jsx } from "@emotion/react";
import {
  Button,
  Grid,
  GridItem,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  NumberIncrementStepper,
  NumberDecrementStepper,
  Heading,
  Input,
  Center,
  Spinner,
  Text,
  Flex,
} from "@chakra-ui/react";
import { useSubscriptions } from "../core/hooks";
import { Fragment } from "react";
import { useForm } from "react-hook-form";

const ManageSubscription = ({ groupId, onAddSeatsClose }) => {
  const { manageSubscriptionMutation, subscriptionsCache } = useSubscriptions(
    groupId
  );

  const {
    handleSubmit: addSeatsHandleSubmit,
    register: addSeatsRegister,
  } = useForm();

  const {
    handleSubmit: addEventsHandleSubmit,
    register: addEventsRegister,
  } = useForm();

  const updateSubscriptionHandler = ({ groupId, units, planType }) => {
    const desiredUnits = Math.trunc(units);
    manageSubscriptionMutation.manageSubscription({
      groupId,
      desiredUnits,
      planType,
    });
    onAddSeatsClose();
  };

  if (subscriptionsCache.isLoading)
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

  const eventPlan = subscriptionsCache.data.find(
    (subscription) => subscription.plan_type === "events"
  );
  const seatPlan = subscriptionsCache.data.find(
    (subscription) => subscription.plan_type === "seats"
  );
  return (
    <Fragment>
      <Heading mt={2} as="h2" fontSize={["lg", "xl"]}>
        Total number of seats?
      </Heading>
      <form onSubmit={addSeatsHandleSubmit(updateSubscriptionHandler)}>
        <Input
          type="hidden"
          name="groupId"
          ref={addSeatsRegister}
          defaultValue={groupId}
        />
        <Input
          type="hidden"
          name="planType"
          ref={addSeatsRegister}
          defaultValue="seats"
        />

        <NumberInput
          defaultValue={seatPlan?.units ? seatPlan.units : "5"}
          min={5}
          size="md"
        >
          <NumberInputField name="units" ref={addSeatsRegister} />
          <NumberInputStepper>
            <NumberIncrementStepper />
            <NumberDecrementStepper />
          </NumberInputStepper>
        </NumberInput>
        <Grid
          templateColumns="repeat(8, 1fr)"
          gap={1}
          alignItems="baseline"
          mt="1"
        >
          <GridItem colSpan={7} />
          <GridItem>
            <Button
              mt={4}
              variant="outline"
              colorScheme="suggested"
              type="submit"
            >
              Update seats
            </Button>
          </GridItem>
        </Grid>
      </form>
      <form onSubmit={addEventsHandleSubmit(updateSubscriptionHandler)}>
        <Heading mt={2} as="h2" fontSize={["lg", "xl"]} pt={16}>
          Number of reports
        </Heading>
        <Input
          type="hidden"
          name="groupId"
          ref={addEventsRegister}
          defaultValue={groupId}
        />
        <Input
          type="hidden"
          name="planType"
          ref={addEventsRegister}
          defaultValue="events"
        />

        <Flex direction={["column", "row", null, "row"]}>
          <NumberInput
            w={["100%", "100%", null, "30%"]}
            minW="10rem"
            defaultValue={eventPlan?.units ? eventPlan.units : "5"}
            min={5}
            size="md"
            precision={0}
            step={1}
          >
            <NumberInputField name="units" ref={addEventsRegister} />
            <NumberInputStepper>
              <NumberIncrementStepper />
              <NumberDecrementStepper />
            </NumberInputStepper>
          </NumberInput>
          <Text ml={4} fontWeight="700" fontSize="xl">
            x1000 Reports/Month
          </Text>
        </Flex>
        <Grid
          templateColumns="repeat(8, 1fr)"
          gap={1}
          alignItems="baseline"
          mt="1"
        >
          <GridItem colSpan={7} />
          <GridItem>
            <Button
              mt={4}
              variant="outline"
              colorScheme="suggested"
              type="submit"
            >
              Update reports
            </Button>
          </GridItem>
        </Grid>
      </form>
    </Fragment>
  );
};

export default ManageSubscription;
