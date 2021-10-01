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

	return {
		apiServerStatus,
		apiServerData,
		crawlersServerStatus,
		crawlersServerData,
		dbServerStatus,
		dbServerData
	};
};

export default useStatus;
