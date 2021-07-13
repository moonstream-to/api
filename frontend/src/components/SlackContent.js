
import { jsx } from "@emotion/react";
import { Link, Text, Image } from "@chakra-ui/react";
const Topics = [
  {
    title: "Welcome!",
    body: [
      {
        text: [
          <Text key={"slack-welcome-content-1"}>
            If you just installed Bugout, thank you for becoming a part of our
            community!
          </Text>,
          <Text key={"slack-welcome-content-2"}>
            <b>@bugout</b> turns your Slack workspace into a knowledge base.
            Keep reading to learn how.
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
          <Text key={"slack-welcome-content-3"}>
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
          "You can also reach us on the Bugout community Slack channel. Direct message Neeraj (@zomglings) or Sophia (@Sophia).",
        ],
      },
    ],
  },
  {
    title: "Using @bugout",
    body: [
      {
        text: [
          <Text key={"slack-welcome-content-4"}>
            The <b>@bugout</b> bot does not know about conversations in channels
            that it has not been invited to. To invite <b>@bugout</b> to a
            channel, simply mention it in that channel:
          </Text>,
        ],
      },
      {
        image: {
          path: "/images/welcome/slack/image1.png",
          annotation: "Mention it in that channel and hit Enter.",
        },
      },
      {
        text: ["and hit Enter. You will see a prompt like this:"],
      },
      {
        image: {
          path: "/images/welcome/slack/image5.png",
          annotation: "Invite slack modal",
        },
      },
      {
        text: [
          <Text key={"slack-welcome-content-5"}>
            Click “Invite to Channel”. Once you have successfully added{" "}
            <b>@bugout</b> to a channel, you will see a message like the one
            below:
          </Text>,
        ],
      },
      {
        image: {
          path: "/images/welcome/slack/image2.png",
          annotation: "Invite slack modal",
        },
      },
    ],
  },
  {
    title: "Creating your team knowledge base",
    body: [
      {
        text: [
          <Text key={"slack-welcome-content-6"}>
            You can work with your team knowledge base from the Bugout web app
            by going to{" "}
            <Link color="primary.400" href="https://bugout.dev">
              https://bugout.dev
            </Link>{" "}
            and registering for an account using the “Register” button at the
            top right
          </Text>,
        ],
      },
      {
        image: {
          path: "/images/welcome/slack/image9.png",
          annotation: "Bugout header",
        },
      },
      {
        text: [
          "Once you have a Bugout account, you can connect it to your Slack knowledge base by going back into Slack, starting a direct message with Bugout (under Apps):",
        ],
      },
      {
        image: {
          path: "/images/welcome/slack/image3.png",
          annotation: "slack bugout",
        },
      },
      {
        text: [
          "and typing:",
          <Text key={"slack-welcome-content-7"}>
            <b>@bugout</b> admin authorize {`<your Bugout username>`}
          </Text>,
        ],
      },
      {
        image: {
          path: "/images/welcome/slack/image10.png",
          annotation: "authorize bugout",
        },
      },
      {
        text: ["If this is successful, you will see a thread like this:"],
      },
      {
        image: {
          path: "/images/welcome/slack/image13.png",
          annotation: "authorize bugout resopnse",
        },
      },
      {
        text: [
          "After this, you will see your team knowledge base under the “Journals” tab on the Bugout website.",
        ],
      },
    ],
  },
  {
    title: "Adding knowledge!",
    body: [
      {
        text: [
          "There are multiple ways of adding knowledge to your Bugout team knowledge base",
        ],
      },
      {
        title: "From the Bugout website",
        body: [
          {
            image: {
              path: "/images/welcome/slack/image7.gif",
              annotation: "website adding knowledge",
            },
          },
        ],
      },
      {
        title: "From Slack using the global shortcut",
        body: [
          {
            image: {
              path: "/images/welcome/slack/image8.gif",
              annotation: "slack adding knowledge",
            },
          },
        ],
      },
      {
        title: "From Slack using the bugout emoji",
        body: [
          {
            text: [
              <Text key={"slack-welcome-content-8"}>
                If you have added the{" "}
                <Image
                  display="inline-block"
                  width="28px"
                  src="/images/logo.png"
                  alt="emoji ant"
                />
                bugout emoji to your Slack workspace, you can react to messages
                with it to add them into your team’s knowledge base:
              </Text>,
            ],
          },
          {
            image: {
              path: "/images/welcome/slack/image11.gif",
              annotation: "slack adding knowledge",
            },
          },
        ],
      },
    ],
  },
  {
    title: "Discovering knowledge",
    body: [
      {
        text: [
          "Any knowledge you add to your knowledge base is immediately accessible and discoverable to you, wherever you work.",
        ],
      },
      {
        title: "From the Bugout website",
        body: [
          {
            image: {
              path: "/images/welcome/slack/image6.png",
              annotation: "website knowledge",
            },
          },
        ],
      },
      {
        title: "From Slack using the global shortcut",
        body: [
          {
            image: {
              path: "/images/welcome/slack/image12.gif",
              annotation: "slack knowledge",
            },
          },
        ],
      },
      {
        title: "From Slack using @bugout",
        body: [
          {
            image: {
              path: "/images/welcome/slack/image4.gif",
              annotation: "slack command line knowledge",
            },
          },
        ],
      },
    ],
  },
  {
    title: "Installing Bugout",
    body: [
      {
        text: [
          <Link
            key={"slack-welcome-content-9"}
            color="primary.400"
            a
            href="https://slack.com/workspace-signin?redir=%2Foauth%3Fclient_id%3D655293806690.1251550900407%26scope%3Dapp_mentions%253Aread%252Cchannels%253Ahistory%252Cchannels%253Aread%252Cchat%253Awrite%252Cemoji%253Aread%252Cgroups%253Ahistory%252Cgroups%253Aread%252Cim%253Ahistory%252Cim%253Aread%252Cim%253Awrite%252Clinks%253Aread%252Cmpim%253Ahistory%252Cmpim%253Aread%252Creactions%253Aread%252Creactions%253Awrite%252Cusers.profile%253Aread%252Ccommands%26user_scope%3D%26redirect_uri%3D%26state%3D%26granular_bot_scope%3D1%26single_channel%3D0%26install_redirect%3D%26team%3D"
          >
            Click here to install Bugout
          </Link>,
          <Text key={"slack-welcome-content-10"}>
            If you’d like to find out more, reach out to Neeraj{" "}
            <Link
              isExternal
              color="primary.400"
              a
              href="mailto:neeraj@bugout.dev"
            >
              neeraj@bugout.dev
            </Link>{" "}
            and Sophia -{" "}
            <Link color="primary.400" a href="mailto:sophia@bugout.dev">
              sophia@bugout.dev
            </Link>
          </Text>,
        ],
      },
    ],
  },
];
export default Topics;
