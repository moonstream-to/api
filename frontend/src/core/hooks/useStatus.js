import { useMutation } from "react-query"
import { useToast } from "./"
import { AuthService } from "../../core/services"

const useStatus = () => {
	const toast = useToast()

	const {
		mutate: status
	} = useMutation(AuthService.status, {
		onError: (error) => {
			toast(error, "error")
		},
		onSuccess: () => {
			toast("Status got", "success")
		}
	})

	return { status }
}

export default useStatus
