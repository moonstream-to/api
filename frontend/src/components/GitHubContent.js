
import { jsx } from "@emotion/react";
import { Link, Text } from "@chakra-ui/react";
const Topics = [
  {
    title: "Welcome!",
    body: [
      {
        text: [
          <Text key={"github-content-1"}>
            If you just installed Bugout, thank you for becoming a part of our
            community!
          </Text>,
        ],
      },
    ],
  },
  {
    title: "Pull request checklists with @bugout-dev",
    body: [
      {
        text: [
          <Text key={"github-content-2"}>
            Sometimes, you need human oversight on your pull requests before you
            can merge them. This is really useful for pull requests that change
            database schema, introduce new environment variables, or introduce
            changes with security or legal implications.
          </Text>,
          <Text key={"github-content-3"}>
            You can use Bugout to create checklists on your pull requests. Just
            mention{" "}
            <Link
              href="https://github.com/bugout-dev"
              isExternal
              color="primary.400"
            >
              @bugout-dev
            </Link>
            :
          </Text>,
          <Text key={"github-content-4"}>
            <i>@bugout-dev check require something important</i>
          </Text>,
          <Text key={"github-content-5"}>For example:</Text>,
        ],
      },
      {
        image: {
          path: "/images/welcome/github/image2.png",
          annotation: "github example",
        },
      },
      {
        text: [
          <Text key={"github-content-6"}>
            When the manual step is finished, mention <i>@bugout-dev</i> again:
          </Text>,
          <Text key={"github-content-7"}>
            <i>@bugout-dev check accept something important</i>
          </Text>,
          <Text key={"github-content-8"}>
            At any time, you can see the status of your checklist by clicking on
            the <i>Details</i> link next to the <i>@bugout-dev</i> continuous
            integration check.
          </Text>,
          <Text key={"github-content-9"}>This is what it looks like:</Text>,
        ],
      },
      {
        image: {
          path: "/images/welcome/github/image1.png",
          annotation: "github example2",
        },
      },
      {
        text: [
          <Text key={"github-content-10"}>
            Play with @bugout-dev on our demo PR:{" "}
            <Link
              href="https://github.com/bugout-dev/github-demo/pull/2"
              isExternal
              color="primary.400"
            >
              https://github.com/bugout-dev/github-demo/pull/2
            </Link>
          </Text>,
        ],
      },
    ],
  },
  {
    title: "Installing Bugout",
    body: [
      {
        text: [
          <Text key={"github-content-11"}>
            You can install Bugout to your organization or to individual
            repositories. Click here to install:{" "}
            <Link
              href="https://github.com/apps/bugout-dev"
              color="primary.400"
              isExternal
            >
              https://github.com/apps/bugout-dev
            </Link>
          </Text>,
          <Text key={"github-content-12"}>
            To see what else you can do with Bugout on GitHub, check out our
            demo repository:{" "}
            <Link
              href="https://github.com/apps/bugout-dev"
              color="primary.400"
              isExternal
            >
              https://github.com/bugout-dev/github-demo
            </Link>
          </Text>,
        ],
      },
    ],
  },
  {
    title: "Contact us",
    body: [
      {
        text: [
          <Text key={"github-content-13"}>
            If you have any questions or would like to suggest improvements to
            Bugout, you can contact us by email: Neeraj -{" "}
            <Link color="primary.400" href="mailto:neeraj@bugout.dev">
              neeraj@bugout.dev
            </Link>
            , Sophia -{" "}
            <Link color="primary.400" href="mailto:sophia@bugout.dev">
              sophia@bugout.dev
            </Link>
            .
          </Text>,
          <Text key={"github-content-14"}>
            You can also reach us on the{" "}
            <Link
              color="primary.400"
              a
              href="https://join.slack.com/t/bugout-dev/shared_invite/zt-fhepyt87-5XcJLy0iu702SO_hMFKNhQ"
              isExternal
            >
              Bugout community Slack channel
            </Link>
            . Direct message Neeraj (@zomglings) or Sophia (@Sophia).
          </Text>,
        ],
      },
    ],
  },
];

export default Topics;
