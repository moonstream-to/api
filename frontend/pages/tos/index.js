import React from "react";
import { Box, Heading, ListItem, Text, Link } from "@chakra-ui/react";
import { UnorderedList, OrderedList } from "@chakra-ui/react";
import { DEFAULT_METATAGS } from "../../src/core/constants";
import { getLayout, getLayoutProps } from "../../src/layouts/WideInfoPage";

const TermsOfService = () => (
  <Box mt="72px">
    <Box m="auto" mb={8} maxWidth="1238" minHeight="60vh">
      <Heading textAlign="start" my={8} as="h1">
        Moonstream Terms of Service
      </Heading>
      <Text fontSize="md">
        Welcome to Moonstream! Please read these Terms of Service before
        accessing or using Moonstream.
      </Text>
      <Heading mt={4}>Definitions</Heading>
      <OrderedList>
        <ListItem>
          <Text mt={4} fontSize="md">
            {`An "Account" represents your legal relationship with Simiotics, Inc.
              A “User Account” represents an individual User’s authorization to
              log in to and use the Service and serves as a User’s identity on
              Moonstream. “Groups” represent teams of users. A User Account can be a
              member of any number of Groups.`}
          </Text>
        </ListItem>
        <ListItem>
          <Text mt={4} fontSize="md">
            {` The “Agreement” refers, collectively, to all the terms, conditions,
              notices contained or referenced in this document (the “Terms of
              Service” or the "Terms") and all other operating rules, policies
              (including the Moonstream Privacy Statement) and procedures that we
              may publish from time to time on the Website.`}
          </Text>
        </ListItem>
        <ListItem>
          <Text mt={4} fontSize="md">
            {` “Content” refers to content featured or displayed through the
              Website, including without limitation code, text, data, articles,
              images, photographs, graphics, software, applications, packages,
              designs, features, and other materials that are available on the
              Website or otherwise available through the Service. "Content" also
              includes Services. “User-Generated Content” is Content, written or
              otherwise, created or uploaded by our Users. "Your Content" is
              Content that you create or own.`}
          </Text>
        </ListItem>
        <ListItem>
          <Text mt={4} fontSize="md">
            “Moonstream“, “Bugout”, “Simiotics”, “We,” and “Us” refer to
            Simiotics, Inc., as well as our affiliates, directors, subsidiaries,
            contractors, licensors, officers, agents, and employees.
          </Text>
        </ListItem>
        <ListItem>
          <Text mt={4} fontSize="md">
            The “Service” refers to the applications, software, products, and
            services provided by Simiotics.
          </Text>
        </ListItem>
        <ListItem>
          <Text mt={4} fontSize="md">
            “The User,” “You,” and “Your” refer to the individual person,
            company, or organization that has visited or is using the Website or
            Service; that accesses or uses any part of the Account; or that
            directs the use of the Account in the performance of its functions.
            A User must be at least 13 years of age.
          </Text>
        </ListItem>
        <ListItem>
          <Text mt={4} fontSize="md">
            The “Website” refers to Moonstream’s website located at
            moonstream.to, and all content, services, and products provided by
            Moonstream at or through the Website. It also refers to subdomains
            of moonstream.to, such as blog.moonstream.to. Occasionally, websites
            owned by Moonstream may provide different or additional terms of
            service. If those additional terms conflict with this Agreement, the
            more specific terms apply to the relevant page or service.
          </Text>
        </ListItem>
      </OrderedList>
      <Heading mt={4}>Account Terms</Heading>
      <Heading as="h3" mt={4} size="md">
        Account Controls
      </Heading>
      <Text mt={4} fontSize="md">
        Subject to these Terms, you retain ultimate administrative control over
        your User Account and the Content within it.
      </Text>
      <Text mt={4} fontSize="md">
        {` The "owner" of a Group that was created under these Terms has ultimate
        administrative control over that Group and the Content within it. Within
        the Service, an owner can manage User access to the Group’s data and
        projects. A Group may have multiple owners, but there must be at least
        one User Account designated as an owner of a Group. If you are the owner
        of an Group under these Terms, we consider you responsible for the
        actions that are performed on or through that Group.`}
      </Text>
      <Heading as="h3" mt={4} size="md">
        Required Information
      </Heading>
      <Text mt={4} fontSize="md">
        You must provide a valid email address in order to complete the signup
        process. Any other information requested, such as your real name, is
        optional, unless you are accepting these terms on behalf of a legal
        entity (in which case we need more information about the legal entity)
        or if you opt for a paid Account, in which case additional information
        will be necessary for billing purposes.
      </Text>
      <Heading as="h3" mt={4} size="md">
        Account Requirements
      </Heading>
      <Text mt={4} fontSize="md">
        {`We have a few simple rules for User Accounts on Moonstream's Service. You
        must be a human to create an Account. Accounts registered by "bots" or
        other automated methods are not permitted.`}
      </Text>
      <Text mt={4} fontSize="md">
        {`We do permit machine accounts. A machine account is an Account set up by
        an individual human who accepts the Terms on behalf of the Account,
        provides a valid email address, and is responsible for its actions. A
        machine account is used exclusively for performing automated tasks.
        Multiple users may direct the actions of a machine account, but the
        owner of the Account is ultimately responsible for the machine's
        actions. You may maintain no more than one free machine account in
        addition to your free User Account.`}
      </Text>
      <Text mt={4} fontSize="md">
        {`One person or legal entity may maintain no more than one free Account
        (if you choose to control a machine account as well, that's fine, but it
        can only be used for running a machine).`}
      </Text>
      <Text mt={4} fontSize="md">
        You must be age 13 or older. If we learn of any User under the age of
        13, we will terminate that User’s Account immediately. If you are a
        resident of a country outside the United States, your country’s minimum
        age may be older; in such a case, you are responsible for complying with
        your country’s laws.
      </Text>
      <Text mt={4} fontSize="md">
        Your login may only be used by one person — i.e., a single login may not
        be shared by multiple people.
      </Text>
      <Text mt={4} fontSize="md">
        A paid Group may only provide access to as many User Accounts as your
        subscription allows.
      </Text>
      <Heading as="h3" mt={4} size="md">
        User Account Security
      </Heading>
      <Text mt={4} fontSize="md">
        You are responsible for keeping your Account secure while you use our
        Service. The content of your Account and its security are up to you. You
        are responsible for all content posted and activity that occurs under
        your Account. You are responsible for maintaining the security of your
        Account and password. Moonstream cannot and will not be liable for any
        loss or damage from your failure to comply with this security
        obligation.
      </Text>
      <Text mt={4} fontSize="md">
        You will promptly notify Moonstream if you become aware of any
        unauthorized use of, or access to, our Service through your Account,
        including any unauthorized use of your password or Account.
      </Text>
      <Heading mt={4}>Acceptable Use</Heading>
      <Text mt={4} fontSize="md">
        Your use of the Website and Service must not violate any applicable
        laws, including copyright or trademark laws, export control or sanctions
        laws, or other laws in your jurisdiction. You are responsible for making
        sure that your use of the Service is in compliance with laws and any
        applicable regulations.
      </Text>
      <Heading mt={4}>User-Generated Content</Heading>
      <Heading as="h3" mt={4} size="md">
        Responsibility for User-Generated Content
      </Heading>
      <Text mt={4} fontSize="md">
        You may create or upload User-Generated Content while using the Service.
        You are solely responsible for the content of, and for any harm
        resulting from, any User-Generated Content that you post, upload, link
        to or otherwise make available via the Service, regardless of the form
        of that Content. We are not responsible for any public display or misuse
        of your User-Generated Content.
      </Text>
      <Heading as="h3" mt={4} size="md">
        Moonstream May Remove Content
      </Heading>
      <Text mt={4} fontSize="md">
        We have the right to refuse or remove any User-Generated Content that,
        in our sole discretion, violates any laws or Moonstream terms or
        policies.
      </Text>
      <Heading as="h3" mt={4} size="md">
        Ownership of Content, Right to Post, and License Grants
      </Heading>
      <Text mt={4} fontSize="md">
        {`You retain ownership of and responsibility for Your Content. If you're
        posting anything you did not create yourself or do not own the rights
        to, you agree that you are responsible for any Content you post; that
        you will only submit Content that you have the right to post; and that
        you will fully comply with any third party licenses relating to Content
        you post.`}
      </Text>
      <Text mt={4} fontSize="md">
        Because you retain ownership of and responsibility for Your Content, we
        need you to grant us — and other Moonstream Users — certain legal
        permissions. These license grants apply to Your Content. If you upload
        Content that already comes with a license granting Moonstream the
        permissions we need to run our Service, no additional license is
        required. You understand that you will not receive any payment for any
        of these granted rights. The licenses you grant to us will end when you
        remove Your Content from our servers, unless other Users have cloned it.
      </Text>

      <Text as="h3" mt={4} size="md">
        License Grant to Us
      </Text>

      <Text mt={4} fontSize="md">
        We need the legal right to do things like host Your Content, publish it,
        and share it. You grant us and our legal successors the right to store,
        archive, parse, and display Your Content, and make incidental copies, as
        necessary to provide the Service, including improving the Service over
        time. This license includes the right to do things like copy it to our
        database and make backups; show it to you and other users; parse it into
        a search index or otherwise analyze it on our servers; share it with
        other users; and perform it, in case Your Content is something like
        music or video. This license does not grant Moonstream the right to sell
        Your Content. It also does not grant Moonstream the right to otherwise
        distribute or use Your Content outside of our provision of the Service.
      </Text>
      <Heading as="h3" mt={4} size="md">
        License Grant to Other Users
      </Heading>

      <Text mt={4} fontSize="md">
        {`Any User-Generated Content you post publicly may be viewed by others. By
        setting your content to be viewed publicly, you agree to allow others to
        view and "clone" your content (this means that others may make their own
        copies of Your Content). If you set your Content to be viewed publicly,
        you grant each User of Moonstream a nonexclusive, worldwide license to use,
        display, and perform Your Content through the Moonstream Service and to
        reproduce Your Content solely on Moonstream as permitted through Moonstream's
        functionality (for example, through cloning). If you are uploading
        Content you did not create or own, you are responsible for ensuring that
        the Content you upload is licensed under terms that grant these
        permissions to other Moonstream Users.`}
      </Text>
      <Heading as="h3" mt={4} size="md">
        Moral Rights
      </Heading>

      <Text mt={4} fontSize="md">
        You retain all moral rights to Your Content that you upload, publish, or
        submit to any part of the Service, including the rights of integrity and
        attribution. However, you waive these rights and agree not to assert
        them against us, to enable us to reasonably exercise the rights granted
        above, but not otherwise.
      </Text>
      <Text mt={4} fontSize="md">
        To the extent this agreement is not enforceable by applicable law, you
        grant Moonstream the rights we need to use Your Content without
        attribution and to make reasonable adaptations of Your Content as
        necessary to render the Website and provide the Service.
      </Text>
      <Heading mt={4}>Private Content</Heading>
      <Heading as="h3" mt={4} size="md">
        Control of Private Content
      </Heading>
      <Text mt={4} fontSize="md">
        Some Accounts may have private content -- for example, groups or
        journals -- which allow the User to control access to Content.
      </Text>
      <Heading as="h3" mt={4} size="md">
        Confidentiality of Private Content
      </Heading>
      <Text mt={4} fontSize="md">
        Moonstream considers private content to be confidential to you.
        Moonstream will protect the contents of private repositories from
        unauthorized use, access, or disclosure in the same manner that we would
        use to protect our own confidential information of a similar nature and
        in no event with less than a reasonable degree of care.
      </Text>
      <Heading as="h3" mt={4} size="md">
        Access
      </Heading>
      <Text mt={4} fontSize="md">
        Moonstream personnel may only access the content of your private content
        in the situations described in our{" "}
        <Link color="primary.600" href="/privacy-policy">
          Privacy Policy
        </Link>
        .
      </Text>
      <Text mt={4} fontSize="md">
        Additionally, we may be compelled by law to disclose your private
        content.
      </Text>
      <Heading mt={4}>Intellectual Property Notice</Heading>
      <Heading as="h3" mt={4} size="md">
        {`Moonstream's Rights to Content`}
      </Heading>
      <Text mt={4} fontSize="md">
        Moonstream and our licensors, vendors, agents, and/or our content
        providers retain ownership of all intellectual property rights of any
        kind related to the Website and Service. We reserve all rights that are
        not expressly granted to you under this Agreement or by law.
      </Text>
      <Heading mt={4}>API Terms</Heading>
      <Text mt={4} fontSize="md">
        {`Abuse or excessively frequent requests to Moonstream via the API may result
        in the temporary or permanent suspension of your Account's access to the
        API. Moonstream, in our sole discretion, will determine abuse or excessive
        usage of the API. We will make a reasonable attempt to warn you via
        email prior to suspension.`}
      </Text>
      <Text mt={4} fontSize="md">
        {`You may not share API tokens to exceed Moonstream's rate limitations.`}
      </Text>
      <Text mt={4} fontSize="md">
        {`You may not use the API to download data or Content from Moonstream for
        spamming purposes, including for the purposes of selling Moonstream users'
        personal information, such as to recruiters, headhunters, and job
        boards.`}
      </Text>
      <Text mt={4} fontSize="md">
        All use of the Moonstream API is subject to these Terms of Service and
        the Moonstream{" "}
        <Link color="primary.600" href="/privacy-policy">
          Privacy Policy
        </Link>
        .
      </Text>
      <Text mt={4} fontSize="md">
        {`Moonstream may offer subscription-based access to our API for those Users
        who require high- throughput access or access that would result in
        resale of Moonstream's Service.`}
      </Text>
      <Heading mt={4}>Payment</Heading>
      <Heading as="h3" mt={4} size="md">
        Pricing
      </Heading>
      <Text mt={4} fontSize="md">
        If you agree to a subscription price, that will remain your price for
        the duration of the payment term; however, prices are subject to change
        at the end of a payment term.
      </Text>
      <Heading as="h3" mt={4} size="md">
        Authorization
      </Heading>
      <Text mt={4} fontSize="md">
        By agreeing to these Terms, you are giving us permission to charge your
        on-file credit card, PayPal account, or other approved methods of
        payment for fees that you authorize for Moonstream.
      </Text>
      <Heading as="h3" mt={4} size="md">
        Responsibility for Payment
      </Heading>
      <Text mt={4} fontSize="md">
        You are responsible for all fees, including taxes, associated with your
        use of the Service. By using the Service, you agree to pay Moonstream
        any charge incurred in connection with your use of the Service. If you
        dispute the matter, contact us. You are responsible for providing us
        with a valid means of payment for paid Accounts. Free Accounts are not
        required to provide payment information.
      </Text>
      <Heading mt={4}>Cancellation and Termination</Heading>
      <Heading as="h3" mt={4} size="md">
        Account Cancellation
      </Heading>
      <Text mt={4} fontSize="md">
        It is your responsibility to properly cancel your Account with
        Moonstream. You can cancel your Account at any time by contacting us by
        email (info@moonstream.to).
      </Text>
      <Heading as="h3" mt={4} size="md">
        Upon Cancellation
      </Heading>
      <Text mt={4} fontSize="md">
        We will retain and use your information as necessary to comply with our
        legal obligations, resolve disputes, and enforce our agreements, but
        barring legal requirements, we will delete your full profile and the
        Content of your repositories within 90 days of cancellation or
        termination (though some information may remain in encrypted backups).
        This information can not be recovered once your Account is cancelled.
      </Text>
      <Text mt={4} fontSize="md">
        We will not delete Content that you have contributed to Groups or that
        other Users have cloned.
      </Text>
      <Text mt={4} fontSize="md">
        Upon request, we will make a reasonable effort to provide an Account
        owner with a copy of your lawful, non-infringing Account contents after
        Account cancellation, termination, or downgrade.
      </Text>
      <Text mt={4} fontSize="md">
        You must make this request within 90 days of cancellation, termination,
        or downgrade.
      </Text>
      <Heading as="h3" mt={4} size="md">
        Moonstream May Terminate
      </Heading>
      <Text mt={4} fontSize="md">
        Moonstream has the right to suspend or terminate your access to all or
        any part of the Website at any time, with or without cause, with or
        without notice, effective immediately.
      </Text>
      <Text mt={4} fontSize="md">
        Moonstream reserves the right to refuse service to anyone for any reason
        at any time.
      </Text>
      <Heading as="h3" mt={4} size="md">
        Survival
      </Heading>
      <Text mt={4} fontSize="md">
        All provisions of this Agreement which, by their nature, should survive
        termination will survive termination — including, without limitation:
        ownership provisions, warranty disclaimers, indemnity, and limitations
        of liability.
      </Text>
      <Heading mt={4}>Communications with Moonstream</Heading>
      <Text mt={4} fontSize="md">
        For contractual purposes, you (1) consent to receive communications from
        us in an electronic form via the email address you have submitted or via
        the Service; and (2) agree that all Terms of Service, agreements,
        notices, disclosures, and other communications that we provide to you
        electronically satisfy any legal requirement that those communications
        would satisfy if they were on paper. This section does not affect your
        non-waivable rights.
      </Text>
      <Heading mt={4}>Disclaimer of Warranties</Heading>
      <Text mt={4} fontSize="md">
        Moonstream provides the Website and the Service “as is” and “as
        available,” without warranty of any kind. Without limiting this, we
        expressly disclaim all warranties, whether express, implied or
        statutory, regarding the Website and the Service including without
        limitation any warranty of merchantability, fitness for a particular
        purpose, title, security, accuracy and non-infringement.
      </Text>
      <Text mt={4} fontSize="md">
        Moonstream does not warrant that the Service will meet your
        requirements; that the Service will be uninterrupted, timely, secure, or
        error-free; that the information provided through the Service is
        accurate, reliable or correct; that any defects or errors will be
        corrected; that the Service will be available at any particular time or
        location; or that the Service is free of viruses or other harmful
        components. You assume full responsibility and risk of loss resulting
        from your downloading and/or use of files, information, content or other
        material obtained from the Service.
      </Text>
      <Heading mt={4}>Limitation of Liability</Heading>
      <Text mt={4} fontSize="md">
        You understand and agree that we will not be liable to you or any third
        party for any loss of profits, use, goodwill, or data, or for any
        incidental, indirect, special, consequential or exemplary damages,
        however arising, that result from the use, disclosure, or display of
        your:
      </Text>
      <UnorderedList pl={3}>
        <ListItem>
          <Text mt={4} fontSize="md">
            User-Generated Content;
          </Text>
        </ListItem>
        <ListItem>
          <Text mt={4} fontSize="md">
            your use or inability to use the Service;
          </Text>
        </ListItem>
        <ListItem>
          <Text mt={4} fontSize="md">
            any modification, price change, suspension or discontinuance of the
            Service;
          </Text>
        </ListItem>
        <ListItem>
          <Text mt={4} fontSize="md">
            the Service generally or the software or systems that make the
            Service available;
          </Text>
        </ListItem>
        <ListItem>
          <Text mt={4} fontSize="md">
            unauthorized access to or alterations of your transmissions or data;
          </Text>
        </ListItem>
        <ListItem>
          <Text mt={4} fontSize="md">
            statements or conduct of any third party on the Service;
          </Text>
        </ListItem>
        <ListItem>
          <Text mt={4} fontSize="md">
            any other user interactions that you input or receive through your
            use of the Service;
          </Text>
        </ListItem>
        <ListItem>
          <Text mt={4} fontSize="md">
            or any other matter relating to the Service.
          </Text>
        </ListItem>
      </UnorderedList>
      <Text mt={4} fontSize="md">
        Our liability is limited whether or not we have been informed of the
        possibility of such damages, and even if a remedy set forth in this
        Agreement is found to have failed of its essential purpose. We will have
        no liability for any failure or delay due to matters beyond our
        reasonable control.
      </Text>
      <Heading mt={4}>Release and Indemnification</Heading>
      <Text mt={4} fontSize="md">
        If you have a dispute with one or more Users, you agree to release
        Moonstream from any and all claims, demands and damages (actual and
        consequential) of every kind and nature, known and unknown, arising out
        of or in any way connected with such disputes.
      </Text>
      <Text mt={4} fontSize="md">
        You agree to indemnify us, defend us, and hold us harmless from and
        against any and all claims, liabilities, and expenses, including
        attorneys’ fees, arising out of your use of the Website and the Service,
        including but not limited to your violation of this Agreement, provided
        that Moonstream (1) promptly gives you written notice of the claim,
        demand, suit or proceeding; (2) gives you sole control of the defense
        and settlement of the claim, demand, suit or proceeding (provided that
        you may not settle any claim, demand, suit or proceeding unless the
        settlement unconditionally releases Moonstream of all liability); and
        (3) provides to you all reasonable assistance, at your expense.
      </Text>
      <Heading mt={4}>Changes to These Terms</Heading>
      <Text mt={4} fontSize="md">
        {`We reserve the right, at our sole discretion, to amend these Terms of
        Service at any time and will update these Terms of Service in the event
        of any such amendments. We will notify our Users of material changes to
        this Agreement, such as price increases, at least 30 days prior to the
        change taking effect by posting a notice on our Website or sending email
        to the primary email address specified in your Moonstream account.
        Customer's continued use of the Service after those 30 days constitutes
        agreement to those revisions of this Agreement. For any other
        modifications, your continued use of the Website constitutes agreement
        to our revisions of these Terms of Service.`}
      </Text>
      <Heading mt={4}>Miscellaneous</Heading>
      <Heading as="h3" mt={4} size="md">
        Governing Law
      </Heading>
      <Text mt={4} fontSize="md">
        Except to the extent applicable law provides otherwise, this Agreement
        between you and Moonstream and any access to or use of the Website or
        the Service are governed by the federal laws of the United States of
        America and the laws of the State of California, without regard to
        conflict of law provisions. You and Moonstream agree to submit to the
        exclusive jurisdiction and venue of the courts located in the City and
        County of San Francisco, California.
      </Text>
      <Heading as="h3" mt={4} size="md">
        Non-Assignability
      </Heading>
      <Text mt={4} fontSize="md">
        Moonstream may assign or delegate these Terms of Service and/or the
        Moonstream
        <Link color="primary.600" href="/privacy-policy">
          {" "}
          Privacy Policy
        </Link>
        , in whole or in part, to any person or entity at any time with or
        without your consent. You may not assign or delegate any rights or
        obligations under the Terms of Service or Privacy Statement without our
        prior written consent, and any unauthorized assignment and delegation by
        you is void.
      </Text>
      <Text mt={4} size="md">
        Severability, No Waiver, and Survival
      </Text>
      <Text mt={4} fontSize="md">
        If any part of this Agreement is held invalid or unenforceable, that
        portion of the Agreement will be construed to reflect the parties’
        original intent. The remaining portions will remain in full force and
        effect. Any failure on the part of Moonstream to enforce any provision
        of this Agreement will not be considered a waiver of our right to
        enforce such provision. Our rights under this Agreement will survive any
        termination of this Agreement.
      </Text>
      <Text mt={4} size="md">
        Amendments; Complete Agreement
      </Text>
      <Text mt={4} fontSize="md">
        This Agreement may only be modified by a written amendment signed by an
        authorized representative of Moonstream, or by the posting by Moonstream
        of a revised version in accordance with Section Q. Changes to These
        Terms. These Terms of Service, together with the Moonstream{" "}
        <Link color="primary.600" href="/privacy-policy">
          Privacy Policy
        </Link>
        , represent the complete and exclusive statement of the agreement
        between you and us. This Agreement supersedes any proposal or prior
        agreement oral or written, and any other communications between you and
        Moonstream relating to the subject matter of these terms including any
        confidentiality or nondisclosure agreements.
      </Text>
    </Box>
  </Box>
);

TermsOfService.getLayout = getLayout;

export async function getStaticProps() {
  const layoutProps = getLayoutProps();
  const metaTags = {
    title: "Moonstream: terms of service",
    description: "Terms of service and legal information",
    keywords: "moonstream, terms of service, legal",
    url: "https://www.moonstream.to/tos",
  };
  layoutProps.props.metaTags = {
    ...layoutProps.props.metaTags,
    ...DEFAULT_METATAGS,
    ...metaTags,
  };
  return { ...layoutProps };
}

export default TermsOfService;
