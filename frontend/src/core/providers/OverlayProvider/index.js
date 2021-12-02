import React, {
  useState,
  useLayoutEffect,
  useContext,
  Suspense,
  useEffect,
} from "react";
import OverlayContext from "./context";
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
  Divider,
} from "@chakra-ui/react";
import UserContext from "../UserProvider/context";
import UIContext from "../UIProvider/context";
import useDashboard from "../../hooks/useDashboard";
import SignUp from "../../../components/SignUp";
import NewDashboardElement from "../../../components/NewDashboardChart";
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

const UploadABI = React.lazy(() => import("../../../components/UploadABI"));

const OverlayProvider = ({ children }) => {
  const { createDashboard } = useDashboard();
  const ui = useContext(UIContext);
  const { user } = useContext(UserContext);
  const [modal, toggleModal] = useState({
    type: MODAL_TYPES.OFF,
    props: undefined,
  });
  const [drawer, toggleDrawer] = useState({
    type: DRAWER_TYPES.OFF,
    props: undefined,
  });
  const [alertCallback, setAlertCallback] = useState(null);
  const drawerDisclosure = useDisclosure();
  const modalDisclosure = useDisclosure();
  const alertDisclosure = useDisclosure();

  useLayoutEffect(() => {
    if (modal.type === MODAL_TYPES.OFF && modalDisclosure.isOpen) {
      modalDisclosure.onClose();
    } else if (modal.type !== MODAL_TYPES.OFF && !modalDisclosure.isOpen) {
      modalDisclosure.onOpen();
    }
  }, [modal.type, modalDisclosure]);

  useLayoutEffect(() => {
    if (drawer.type === DRAWER_TYPES.OFF && drawerDisclosure.isOpen) {
      drawerDisclosure.onClose();
    } else if (drawer.type !== DRAWER_TYPES.OFF && !drawerDisclosure.isOpen) {
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

  console.assert(
    Object.values(DRAWER_TYPES).some((element) => element === drawer.type)
  );
  console.assert(
    Object.values(MODAL_TYPES).some((element) => element === modal.type)
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
      !modal.type
    ) {
      toggleModal({ type: MODAL_TYPES.LOGIN });
    } else if (user && ui.isLoggingOut) {
      toggleModal({ type: MODAL_TYPES.OFF });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ui.isAppView, ui.isAppReady, user, ui.isLoggingOut, modal.type]);

  const finishNewDashboard = () => {
    toggleDrawer({ type: DRAWER_TYPES.OFF, props: undefined });
    window.sessionStorage.removeItem("new_dashboard");
  };

  const submitNewDashboard = () => {
    const dashboardState = JSON.parse(sessionStorage.getItem("new_dashboard"));
    createDashboard.mutate({
      name: dashboardState.name,
      subscriptions: dashboardState.subscriptions.map((pickedSubscription) => {
        const retval = {
          subscription_id: pickedSubscription.subscription_id,
          generic: [],
          all_methods: !!pickedSubscription.isMethods,
          all_events: !!pickedSubscription.isEvents,
        };

        pickedSubscription.generic.transactions.in &&
          retval.generic.push({ name: "transactions_in" });
        pickedSubscription.generic.transactions.out &&
          retval.generic.push({ name: "transactions_out" });
        pickedSubscription.generic.value.in &&
          retval.generic.push({ name: "value_in" });
        pickedSubscription.generic.value.out &&
          retval.generic.push({ name: "value_out" });
        pickedSubscription.generic.balance &&
          retval.generic.push({ name: "balance" });
        retval["methods"] = [];
        retval["events"] = [];

        return retval;
      }),
    });
  };

  const submitNewDashboardItem = () => {
    console.log("submit new dashboard item");
  };
  useEffect(() => {
    if (createDashboard.isSuccess) {
      finishNewDashboard();
    }
  }, [createDashboard.isSuccess]);
  return (
    <OverlayContext.Provider
      value={{ modal, toggleModal, drawer, toggleDrawer, toggleAlert }}
    >
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
        onClose={() => toggleModal({ type: MODAL_TYPES.OFF })}
        size="2xl"
        scrollBehavior="outside"
        trapFocus={false}
      >
        <ModalOverlay />

        <ModalContent>
          <ModalHeader bgColor="white.200" py={2} fontSize="lg">
            {modal.type === MODAL_TYPES.NEW_SUBSCRIPTON &&
              "Subscribe to a new address"}
            {modal.type === MODAL_TYPES.FORGOT && "Forgot Password"}
            {modal.type === MODAL_TYPES.HUBSPOT && "Join the waitlist"}
            {modal.type === MODAL_TYPES.LOGIN && "Login now"}
            {modal.type === MODAL_TYPES.SIGNUP && "Create an account"}
            {modal.type === MODAL_TYPES.UPLOAD_ABI && "Assign ABI"}
          </ModalHeader>
          <Divider />
          <ModalCloseButton />
          <ModalBody
            zIndex={100002}
            bgColor={
              modal.type === MODAL_TYPES.UPLOAD_ABI ? "white.200" : undefined
            }
          >
            <Suspense fallback={<Spinner />}>
              {modal.type === MODAL_TYPES.NEW_SUBSCRIPTON && (
                <NewSubscription
                  onClose={() => toggleModal({ type: MODAL_TYPES.OFF })}
                  isModal={true}
                  {...modal.props}
                />
              )}
              {modal.type === MODAL_TYPES.FORGOT && <ForgotPassword />}
              {modal.type === MODAL_TYPES.HUBSPOT && (
                <HubspotForm
                  toggleModal={toggleModal}
                  title={"Join the waitlist"}
                  formId={"1897f4a1-3a00-475b-9bd5-5ca2725bd720"}
                />
              )}
              {modal.type === MODAL_TYPES.LOGIN && (
                <SignIn toggleModal={toggleModal} />
              )}
              {modal.type === MODAL_TYPES.SIGNUP && (
                <SignUp toggleModal={toggleModal} />
              )}
              {modal.type === MODAL_TYPES.UPLOAD_ABI && (
                <UploadABI {...modal.props} />
              )}
            </Suspense>
          </ModalBody>
        </ModalContent>
      </Modal>
      {/* )} */}
      <Drawer
        trapFocus={false}
        isOpen={drawerDisclosure.isOpen}
        placement="right"
        size="xl"
        // w="80%"
        initialFocusRef={firstField}
        onClose={() => toggleAlert(() => finishNewDashboard())}
      >
        <DrawerOverlay />
        <DrawerContent overflowY="scroll">
          <DrawerCloseButton />
          <DrawerHeader borderBottomWidth="1px">
            {drawer.type === DRAWER_TYPES.NEW_DASHBOARD && "New dashboard"}
            {drawer.type === DRAWER_TYPES.NEW_DASHBOARD_ITEM &&
              "New dashboard element"}
          </DrawerHeader>

          <DrawerBody h="auto">
            {drawer.type === DRAWER_TYPES.NEW_DASHBOARD && (
              <Suspense fallback={<Spinner />}>
                <NewDashboard firstField={firstField} props={drawer.props} />
              </Suspense>
            )}
            {drawer.type === DRAWER_TYPES.NEW_DASHBOARD_ITEM && (
              <Suspense fallback={<Spinner />}>
                <NewDashboardElement
                  firstField={firstField}
                  props={drawer.props}
                />
              </Suspense>
            )}
          </DrawerBody>
          <DrawerFooter borderTopWidth="1px">
            <Button
              variant="outline"
              mr={3}
              onClick={() => {
                console.log("cancel click on drawer", drawer.type);
                if (drawer.type === DRAWER_TYPES.NEW_DASHBOARD) {
                  toggleAlert(() => finishNewDashboard());
                }
                if (drawer.type === DRAWER_TYPES.NEW_DASHBOARD_ITEM) {
                  toggleAlert(() =>
                    toggleDrawer({ type: DRAWER_TYPES.OFF, props: undefined })
                  );
                }
              }}
            >
              Cancel
            </Button>
            <Button
              colorScheme="blue"
              isLoading={createDashboard.isLoading}
              onClick={() => {
                drawer.type === DRAWER_TYPES.NEW_DASHBOARD &&
                  submitNewDashboard();
                drawer.type === DRAWER_TYPES.NEW_DASHBOARD_ITEM &&
                  submitNewDashboardItem();
              }}
            >
              Submit
            </Button>
          </DrawerFooter>
        </DrawerContent>
      </Drawer>

      {children}
    </OverlayContext.Provider>
  );
};

export default OverlayProvider;
