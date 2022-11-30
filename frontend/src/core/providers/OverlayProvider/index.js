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
} from "@chakra-ui/react";
import UIContext from "../UIProvider/context";
import useDashboard from "../../hooks/useDashboard";
import SignUp from "../../../components/SignUp";
import NewDashboardChart from "../../../components/NewDashboardChart";
import { useRouter } from "../../hooks";
import { DASHBOARD_UPDATE_ACTIONS } from "../../constants";
import UpdateSubscriptionLabelInput from "../../../components/UpdateSubscriptionLabelInput";
const NewDashboardName = React.lazy(() =>
  import("../../../components/NewDashboardName")
);
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
  const { params } = useRouter();
  const { dashboardId } = params;
  const { createDashboard, updateDashboard, dashboardCache } =
    useDashboard(dashboardId);
  const ui = useContext(UIContext);
  const [modal, toggleModal] = useState({
    type: MODAL_TYPES.OFF,
    props: undefined,
    key: undefined,
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
      modal.type !== MODAL_TYPES.LOGIN &&
      !modalDisclosure.isOpen &&
      ui.isAppView &&
      !ui.isLoggedIn &&
      !ui.isLoggingOut &&
      !ui.isLoggingIn &&
      ui.isAppReady
    ) {
      toggleModal({ type: MODAL_TYPES.LOGIN });
    } else if (
      (modal.type === MODAL_TYPES.LOGIN || modal.type === MODAL_TYPES.SIGNUP) &&
      ui.isLoggedIn
    ) {
      toggleModal({ type: MODAL_TYPES.OFF });
    }
  }, [
    modal.type,
    modalDisclosure,
    ui.isAppView,
    ui.isLoggedIn,
    ui.isLoggingOut,
    ui.isLoggingIn,
    ui.isAppReady,
  ]);

  const finishNewDashboard = () => {
    toggleDrawer({
      type: DRAWER_TYPES.OFF,
      props: dashboardCache.data.resource_data,
    });
    window.sessionStorage.removeItem("new_dashboard");
  };

  const submitNewDashboard = () => {
    const dashboardState = JSON.parse(sessionStorage.getItem("new_dashboard"));
    if (dashboardState) {
      //creating ABI defined dashboard
      createDashboard.mutate({
        name: dashboardState.name,
        subscription_settings: dashboardState.subscription_settings.map(
          (pickedSubscription) => {
            const retval = {
              subscription_id: pickedSubscription.subscription_id,
              generic: [],
              all_methods: false,
              all_events: false,
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
          }
        ),
      });
    } else {
      //creating empty dashboard
      createDashboard.mutate();
    }
  };

  const submitNewDashboardItem = () => {
    updateDashboard.mutate({ dashboard: ui.dashboardUpdate, id: dashboardId });
  };

  useEffect(() => {
    if (
      drawer.type === DRAWER_TYPES.NEW_DASHBOARD_ITEM &&
      updateDashboard.isSuccess
    ) {
      toggleDrawer({ type: DRAWER_TYPES.OFF, props: undefined });
      updateDashboard.reset();
    }
  }, [updateDashboard, drawer.type]);

  useEffect(() => {
    if (
      drawer.type === DRAWER_TYPES.NEW_DASHBOARD &&
      createDashboard.isSuccess
    ) {
      finishNewDashboard();
      createDashboard.reset();
    }
    //eslint-disable-next-line
  }, [createDashboard.isSuccess]);

  useEffect(() => {
    if (
      createDashboard.isSuccess &&
      drawer.type === DRAWER_TYPES.NEW_DASHBOARD_ITEM
    ) {
      toggleDrawer({ type: DRAWER_TYPES.OFF, props: undefined });
    }
  }, [createDashboard.isSuccess, drawer.type]);

  const cancelDashboardItem = () => {
    toggleDrawer({ type: DRAWER_TYPES.OFF, props: undefined });
    ui.dispatchDashboardUpdate({
      type: DASHBOARD_UPDATE_ACTIONS.RESET_TO_DEFAULT,
    });
  };

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
        size={modal.type === MODAL_TYPES.LOGIN ? "lg" : "2xl"}
        scrollBehavior="outside"
        trapFocus={false}
      >
        <ModalOverlay backdropFilter="auto" backdropBrightness="60%" />

        <ModalContent
          bg="black.300"
          borderRadius="15px"
          border="1px white solid"
          p="30px"
          textColor="white"
        >
          <ModalHeader
            p="0px"
            fontSize="24px"
            lineHeight="24px"
            fontWeight="700"
            mb="30px"
          >
            {modal.type === MODAL_TYPES.NEW_SUBSCRIPTON &&
              "Subscribe to a new address"}
            {modal.type === MODAL_TYPES.FORGOT && "Forgot Password"}
            {modal.type === MODAL_TYPES.HUBSPOT && "Join the waitlist"}
            {modal.type === MODAL_TYPES.LOGIN && "Login now"}
            {modal.type === MODAL_TYPES.SIGNUP && "Create an account"}
            {modal.type === MODAL_TYPES.UPLOAD_ABI && "Assign ABI"}
            {modal.type === MODAL_TYPES.NEW_DASHBOARD_FLOW &&
              "Would you like to give it a name?"}
            {modal.type === MODAL_TYPES.MOBILE_INPUT_FIELD && modal.props.title}
          </ModalHeader>
          <ModalCloseButton color="white" top="25px" right="25px" />
          <ModalBody
            p="0px"
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
              {modal.type === MODAL_TYPES.FORGOT && (
                <ForgotPassword toggleModal={toggleModal} />
              )}
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
              {modal.type === MODAL_TYPES.NEW_DASHBOARD_FLOW && (
                <NewDashboardName {...modal.props} />
              )}
              {modal.type === MODAL_TYPES.MOBILE_INPUT_FIELD && (
                <UpdateSubscriptionLabelInput {...modal.props} />
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
        initialFocusRef={firstField}
        onClose={() => {
          switch (drawer.type) {
            case DRAWER_TYPES.NEW_DASHBOARD:
              toggleAlert(() => finishNewDashboard());
              break;
            case DRAWER_TYPES.NEW_DASHBOARD_ITEM:
              cancelDashboardItem();
              break;
          }
        }}
      >
        <DrawerOverlay backdropFilter="auto" backdropBrightness="60%" />
        <DrawerContent overflowY="scroll" textColor="white" bg="black.300">
          <DrawerCloseButton />
          <DrawerHeader borderBottomWidth="1px">
            {drawer.type === DRAWER_TYPES.NEW_DASHBOARD && "New dashboard"}
            {drawer.type === DRAWER_TYPES.NEW_DASHBOARD_ITEM &&
              "Edit dashboard"}
          </DrawerHeader>

          <DrawerBody h="auto">
            {drawer.type === DRAWER_TYPES.NEW_DASHBOARD && (
              <Suspense fallback={<Spinner />}>
                <NewDashboard firstField={firstField} props={drawer.props} />
              </Suspense>
            )}
            {drawer.type === DRAWER_TYPES.NEW_DASHBOARD_ITEM && (
              <Suspense fallback={<Spinner id={"edit  dahsboard fallback"} />}>
                <NewDashboardChart
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
                if (drawer.type === DRAWER_TYPES.NEW_DASHBOARD) {
                  toggleAlert(() => finishNewDashboard());
                }
                if (drawer.type === DRAWER_TYPES.NEW_DASHBOARD_ITEM) {
                  cancelDashboardItem();
                }
              }}
            >
              Cancel
            </Button>
            <Button
              colorScheme="blue"
              onClick={() => {
                drawer.type === DRAWER_TYPES.NEW_DASHBOARD &&
                  submitNewDashboard();
                drawer.type === DRAWER_TYPES.NEW_DASHBOARD_ITEM &&
                  submitNewDashboardItem();
              }}
              isLoading={
                drawer.type === DRAWER_TYPES.NEW_DASHBOARD_ITEM
                  ? updateDashboard.isLoading
                  : createDashboard.isLoading
              }
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
