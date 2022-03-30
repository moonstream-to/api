import React, { useEffect, useState, useContext } from "react";
import { useForm } from "react-hook-form";
import {
  Box
} from "@chakra-ui/react";
import useRouter from "../../src/core/hooks/useRouter";

import Icon from "../../src/components/CustomIcon";
import useSignUp from "../../src/core/hooks/useSignUp";
import useUser from "../../src/core/hooks/useSignUp";
import { DEFAULT_METATAGS } from "../../src/core/constants";
import OverlayContext from "../../src/core/providers/OverlayProvider/context";
import { OnboardOS, useOnboardOS } from 'onboard-os'
import { MODAL_TYPES } from "../../src/core/providers/OverlayProvider/constants";

export async function getStaticProps() {
  return {
    props: { metaTags: { ...DEFAULT_METATAGS } },
  };
}

const SUBSCRIPTION_SCREEN_ID = "31a42b36-7323-4275-9979-c3ab58dba159"
const DASHBOARD_SCREEN_ID = "853b0417-7b6e-450f-8401-6af9f688bb52"

const Register = () => {
  const router = useRouter();
  const onboardos = useOnboardOS()
  const overlay = useContext(OverlayContext);


  const { onStartLoader } = onboardos

  const { handleSubmit, errors, register } = useForm();
  const [showPassword, togglePassword] = useState(false);

  const { user } = useUser();
  const loggedIn = user && user.username;

  //   const { email, code } = router.query;
  const email = router.query?.email;
  const code = router.query?.code;
  const { signUp, isLoading, isSuccess } = useSignUp(code);

  loggedIn && router.push("/stream");

  const onEnd = () => {
    router.push("/welcome", undefined, { shallow: false });
  }

  useEffect(() =>{
    if(isSuccess && !isLoading){
      onboardos.goForward()
      onboardos.stopLoader()
    }

    if(!isLoading && !isSuccess) {
      onboardos.stopLoader()
    }
  }, [isSuccess, isLoading])

  const onValidate = (stepId, stepType, data) => {
    const {user_name, password, email} = data

    try {
      signUp({username: user_name, email, password}).catch(() => {
        onboardos.stopLoader()
      })

      onboardos.startLoader("Creating Account...") 

    }catch(e) {
      onboardos.stopLoader()
    }
  }

  const onAction = (stepId, stepType, data) => {

    if(stepId === SUBSCRIPTION_SCREEN_ID) {
      overlay.toggleModal({
        type: MODAL_TYPES.NEW_SUBSCRIPTON,
        props: undefined,
      })
    }

    if(stepId === DASHBOARD_SCREEN_ID) {
      overlay.toggleModal({
        type: MODAL_TYPES.NEW_DASHBOARD_FLOW,
        props: undefined,
      })

    }
  }

  return (
    <Box minH="900px" w="100%" px={["7%", null, "25%"]} alignSelf="center">
     
      <OnboardOS onAction={onAction} onEnd={onEnd} register={onboardos.register} onValidate={onValidate} apiKey={"mibnpdV2w0pyKhltNEZj"} />

    </Box>
  );
};
export default Register;
