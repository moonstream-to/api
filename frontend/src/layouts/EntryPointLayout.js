import React from "react";

const EntryPointLayout = (props) => {
  return props.children;
};

export const getLayout = (page) => <EntryPointLayout>{page}</EntryPointLayout>;

export default EntryPointLayout;
