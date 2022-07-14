import React from "react";
import { Flex, Heading } from "@chakra-ui/react";

const ExampleCode = () => {
  const HtmlCode = () => {
    return (
      <Flex
        w={["265px", "358px", "auto"]}
        position="relative"
        display="inline-block"
        fontSize={["sm", "md", "lg"]}
      >
        <pre className="js language-js">
          <code className="hljs js language-js">
            <span className="hljs-keyword">{"async"}</span>{" "}
            <span className="hljs-function">
              <span className="hljs-keyword">function</span>{" "}
              <span className="hljs-title">startRandomLootboxOpening</span>
              {"("}
              <span className="hljs-params">lootboxId</span>
              {")"}{" "}
            </span>
            {"{"}
            <br />
            &nbsp; &nbsp;
            <span className="hljs-keyword">{"let"}</span> {"userAddress ="}{" "}
            <span className="hljs-built_in">{"window"}</span>
            {".ethereum.selectedAddress;"}
            <br />
            &nbsp; &nbsp;
            <span className="hljs-keyword">{"let"}</span> activeOpening ={" "}
            <span className="hljs-keyword">{"await"}</span>{" "}
            {"checkUsersActiveLootboxOpeningStatus(userAddress);"}
            <br />
            &nbsp; &nbsp;
            <span className="hljs-keyword">{"if"}</span> (activeOpening !={" "}
            <span className="hljs-literal">null</span>
            {") {"}
            <br />
            &nbsp; &nbsp; &nbsp; &nbsp;
            <span className="hljs-built_in">{"console"}</span>
            {".log"}(
            <span className="hljs-string">
              &quot;User already has active opening&quot;
            </span>
            {");"}
            <br />
            &nbsp; &nbsp; &nbsp; &nbsp;
            <span className="hljs-keyword">{"return"}</span>; <br />
            &nbsp; &nbsp;
            {"}"}
            <br />
            &nbsp; &nbsp;
            <span className="hljs-keyword">const</span> count ={" "}
            <span className="hljs-number">1</span>;{" "}
            <span className="hljs-comment">
              {"// you can open only 1 random lootbox at a time"}
            </span>
            <br />
            &nbsp; &nbsp;
            <span className="hljs-keyword">await</span>{" "}
            openOrdinaryLootbox(lootboxId, count);
            <br />
            {"}"}
          </code>
        </pre>
      </Flex>
    );
  };

  return (
    <Flex
      flexDirection="column"
      textColor="white"
      bgColor="#686464"
      p={["5px", "10px", "25px"]}
      rounded="lg"
    >
      <Heading as="h3" fontSize="lg" pb="20px">
        We make sure our code is easy to use. Here’s an example:
      </Heading>
      <Flex position={"relative"}>
        <HtmlCode />
      </Flex>
    </Flex>
  );
};

export default ExampleCode;
