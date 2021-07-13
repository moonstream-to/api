
import { jsx } from "@emotion/react";
import {
  Box,
  Spinner,
  Center,
  RadioGroup,
  Radio,
  Stack,
  Divider,
} from "@chakra-ui/react";
import { ErrorIndicators } from ".";
import { useMemo, useState } from "react";

//
const ErrorsStats = ({ data, isLoading }) => {
  const [tagType, setTagType] = useState("common");

  const LoadingSpinner = () => (
    <Box px="12%" my={12} width="100%">
      <Center>
        <Spinner
          hidden={false}
          my={0}
          size="lg"
          color="primary.500"
          thickness="4px"
          speed="1.5s"
        />
      </Center>
    </Box>
  );

  const highest_entropy_indicators = useMemo(
    () =>
      data &&
      Object.keys(data?.highest_entropy_tags)?.map((key) => {
        return {
          key: key,
          value: data?.highest_entropy_tags[key],
          timeseries: [...data?.errors_time_series[key]],
        };
      }),
    [data]
  );

  const most_common_indicators = useMemo(
    () =>
      data &&
      Object.keys(data?.most_common_errors)?.map((key) => {
        return {
          key: key,
          value: data?.most_common_errors[key],
          timeseries: [...data?.errors_time_series[key]],
        };
      }),
    [data]
  );

  if (isLoading || !data) return <LoadingSpinner />;

  return (
    <Box w="100%">
      <RadioGroup onChange={setTagType} value={tagType}>
        <Stack direction="row">
          {/* <Radio value="all">all</Radio> */}
          <Radio value="entropy">highest entropy</Radio>
          <Radio value="common">most common</Radio>
        </Stack>
      </RadioGroup>
      <Divider />
      {tagType === "common" && (
        <ErrorIndicators data={most_common_indicators} />
      )}
      {tagType === "entropy" && (
        <ErrorIndicators data={highest_entropy_indicators} />
      )}
    </Box>
  );
};
export default ErrorsStats;
