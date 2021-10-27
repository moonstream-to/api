import React, { useState, useLayoutEffect, useContext, Suspense } from "react";
import ModalContext from "./context";
import { MODAL_TYPES, DRAWER_TYPES } from "./constants";
import {
  Modal,
  ModalOverlay,
  ModalCloseButton,
  ModalBody,
  ModalContent,
  useDisclosure,
  ModalHeader,
  Drawer,
  DrawerBody,
  DrawerFooter,
  DrawerHeader,
  DrawerOverlay,
  DrawerContent,
  DrawerCloseButton,
  AlertDialog,
  AlertDialogBody,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogContent,
  AlertDialogOverlay,
  Button,
  Spinner,
} from "@chakra-ui/react";
import UserContext from "../UserProvider/context";
import UIContext from "../UIProvider/context";
const ForgotPassword = React.lazy(() =>
  import("../../../components/ForgotPassword")
);
const SignIn = React.lazy(() => import("../../../components/SignIn"));
const HubspotForm = React.lazy(() => import("../../../components/HubspotForm"));
const NewDashboard = React.lazy(() =>
  import("../../../components/NewDashboard")
);
const NewSubscription = React.lazy(() =>
  import("../../../components/NewSubscription")
);

const ModalProvider = ({ children }) => {
  const ui = useContext(UIContext);
  const { user } = useContext(UserContext);
  const [modal, toggleModal] = useState(MODAL_TYPES.OFF);
  const [drawer, toggleDrawer] = useState(DRAWER_TYPES.OFF);
  const [alertCallback, setAlertCallback] = useState(null);
  const drawerDisclosure = useDisclosure();
  const modalDisclosure = useDisclosure();
  const alertDisclosure = useDisclosure();

  // TODO @Peersky: This is written to take Disclosure state and modify modal state
  // This should be written same as Drawer - Take modal state and modify Disclosure
  // However to implement this - first SIGNUP,FORGOT,HUBSPOT components should be written to support this
  useLayoutEffect(() => {
    if (modal === MODAL_TYPES.OFF && modalDisclosure.isOpen) {
      // toggleModal(MODAL_TYPES.NEW_SUBSCRIPTON);
      console.log("thats unexpected");
      modalDisclosure.onClose();
    } else if (modal !== MODAL_TYPES.OFF && !modalDisclosure.isOpen) {
      // toggleModal(MODAL_TYPES.OFF);
      modalDisclosure.onOpen();
    }
  }, [modal, modalDisclosure]);

  useLayoutEffect(() => {
    if (drawer === DRAWER_TYPES.OFF && drawerDisclosure.isOpen) {
      drawerDisclosure.onClose();
    } else if (drawer !== DRAWER_TYPES.OFF && !drawerDisclosure.isOpen) {
      drawerDisclosure.onOpen();
    }
  }, [drawer, drawerDisclosure]);

  const handleAlertConfirm = () => {
    alertCallback && alertCallback();
    alertDisclosure.onClose();
  };

  const toggleAlert = (callback) => {
    setAlertCallback(() => callback);
    alertDisclosure.onOpen();
  };

  console.log("drawer", drawer);
  console.assert(
    Object.values(DRAWER_TYPES).some((element) => element === drawer)
  );
  console.log("modal", modal);
  console.assert(
    Object.values(MODAL_TYPES).some((element) => element === modal)
  );

  const cancelRef = React.useRef();
  const firstField = React.useRef();

  useLayoutEffect(() => {
    if (
      ui.isAppView &&
      ui.isInit &&
      !user?.username &&
      !ui.isLoggingOut &&
      !ui.isLoggingIn &&
      !modal
    ) {
      toggleModal(MODAL_TYPES.LOGIN);
    } else if (user && ui.isLoggingOut) {
      toggleModal(MODAL_TYPES.OFF);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ui.isAppView, ui.isAppReady, user, ui.isLoggingOut, modal]);

  return (
    <ModalContext.Provider value={{ modal, toggleModal, drawer, toggleDrawer }}>
      <AlertDialog
        isOpen={alertDisclosure.isOpen}
        leastDestructiveRef={cancelRef}
        // onClose={onClose}
      >
        <AlertDialogOverlay>
          <AlertDialogContent>
            <AlertDialogHeader fontSize="lg" fontWeight="bold">
              Cancel
            </AlertDialogHeader>

            <AlertDialogBody>Are you sure you want to cancel?</AlertDialogBody>

            <AlertDialogFooter>
              <Button ref={cancelRef} onClick={() => alertDisclosure.onClose()}>
                Cancel
              </Button>
              <Button
                colorScheme="red"
                ml={3}
                onClick={() => {
                  handleAlertConfirm();
                }}
              >
                Confirm
              </Button>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialogOverlay>
      </AlertDialog>

      <Modal
        isOpen={modalDisclosure.isOpen}
        onClose={() => toggleModal(MODAL_TYPES.OFF)}
        size="2xl"
        scrollBehavior="outside"
        trapFocus={false}
      >
        <ModalOverlay />

        <ModalContent>
          <ModalHeader>
            {modal === MODAL_TYPES.NEW_SUBSCRIPTON &&
              "Subscribe to a new address"}
            {modal === MODAL_TYPES.FORGOT && "Forgot Password"}
            {modal === MODAL_TYPES.HUBSPOT && "Join the waitlist"}
            {modal === MODAL_TYPES.LOGIN && "Login now"}
            {modal === MODAL_TYPES.SIGNUP && "Create an account"}
          </ModalHeader>
          <ModalCloseButton />
          <ModalBody zIndex={100002}>
            <Suspense fallback={<Spinner />}>
              {modal === MODAL_TYPES.NEW_SUBSCRIPTON && (
                <NewSubscription
                  onClose={() => toggleModal(MODAL_TYPES.OFF)}
                  isModal={true}
                />
              )}
              {modal === MODAL_TYPES.FORGOT && <ForgotPassword />}
              {modal === MODAL_TYPES.HUBSPOT && (
                <HubspotForm
                  toggleModal={toggleModal}
                  title={"Join the waitlist"}
                  formId={"1897f4a1-3a00-475b-9bd5-5ca2725bd720"}
                />
              )}
              {modal === MODAL_TYPES.LOGIN && (
                <SignIn toggleModal={toggleModal} />
              )}
              {
                modal === MODAL_TYPES.SIGNUP && ""
                // <SignUp toggleModal={toggleModal} />
              }
            </Suspense>
          </ModalBody>
        </ModalContent>
      </Modal>
      {/* )} */}
      <Drawer
        isOpen={drawerDisclosure.isOpen}
        placement="right"
        size="xl"
        // w="80%"
        initialFocusRef={firstField}
        onClose={() => toggleAlert(() => toggleDrawer(DRAWER_TYPES.OFF))}
      >
        <DrawerOverlay />
        <DrawerContent>
          <DrawerCloseButton />
          <DrawerHeader borderBottomWidth="1px">
            {DRAWER_TYPES.NEW_DASHBOARD && "New dashboard"}
          </DrawerHeader>

          <DrawerBody>
            {DRAWER_TYPES.NEW_DASHBOARD && (
              <Suspense fallback={<Spinner />}>
                <NewDashboard firstField={firstField} />
              </Suspense>
            )}
          </DrawerBody>
          <DrawerFooter borderTopWidth="1px">
            <Button
              variant="outline"
              mr={3}
              onClick={() => toggleAlert(() => toggleDrawer(DRAWER_TYPES.OFF))}
            >
              Cancel
            </Button>
            <Button
              colorScheme="blue"
              onClick={() => {
                console.log("submit clicked");
              }}
            >
              Submit
            </Button>
          </DrawerFooter>
        </DrawerContent>
      </Drawer>

      {children}
    </ModalContext.Provider>
  );
};

export default ModalProvider;
