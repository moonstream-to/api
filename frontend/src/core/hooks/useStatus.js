import { useMutation } from "react-query";
import { useToast } from "./";
import { AuthService } from "../../core/services";

const useStatus = () => {
	const toast = useToast();

	const { mutate: apiServerStatus, data: apiServerData } = useMutation(
		AuthService.apiServerStatus,
		{
			onError: (error) => {
				// toast(error, "error");
			},
			onSuccess: () => {
				// toast("Status received", "success");
			}
		}
	);

	const { mutate: crawlersServerStatus, data: crawlersServerData } =
		useMutation(AuthService.crawlersServerStatus, {
			onError: (error) => {
				// toast(error, "error");
			},
			onSuccess: () => {
				// toast("Status received", "success");
			}
		});
	const { mutate: gethStatus, data: gethData } = useMutation(
		AuthService.gethStatus,
		{
			onError: (error) => {
				// toast(error, "error");
			},
			onSuccess: () => {
				// toast("Status received", "success");
			}
		}
	);
	const { mutate: crawlersStatus, data: crawlersData } = useMutation(
		AuthService.crawlersStatus,
		{
			onError: (error) => {
				// toast(error, "error");
			},
			onSuccess: () => {
				// toast("Status received", "success");
			}
		}
	);

	const { mutate: dbServerStatus, data: dbServerData } = useMutation(
		AuthService.dbServerStatus,
		{
			onError: (error) => {
				// toast(error, "error");
			},
			onSuccess: () => {
				// toast("Status received", "success");
			}
		}
	);
	const { mutate: latestBlockDBStatus, data: latestBlockDBData } =
		useMutation(AuthService.latestBlockDBStatus, {
			onError: (error) => {
				// toast(error, "error");
			},
			onSuccess: () => {
				// toast("Status received", "success");
			}
		});

	return {
		apiServerStatus,
		apiServerData,
		crawlersServerStatus,
		crawlersServerData,
		gethStatus,
		gethData,
		crawlersStatus,
		crawlersData,
		dbServerStatus,
		dbServerData,
		latestBlockDBStatus,
		latestBlockDBData
	};
};

export default useStatus;
