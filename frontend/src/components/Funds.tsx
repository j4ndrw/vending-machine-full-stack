import { useSnackbar } from "notistack";
import { useState } from "react";
import { useSnapshot } from "valtio";
import { deposit } from "../services/deposit";
import { fetchUser, store } from "../store";
import AddFundsModal from "./AddFundsModal";

function Funds() {
    const { enqueueSnackbar } = useSnackbar();

    const { deposit: credits } = useSnapshot(store);

    const [openModal, setOpenModal] = useState<boolean>(false);

    return (
        <div className="px-16 flex justify-center items-center">
            <div>{credits} credits</div>
            <button
                className="mx-4 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-700 transition duration-150 ease-in-out hover:bg-indigo-600 bg-indigo-700 rounded text-white px-8 py-2 text-sm"
                onClick={() => {
                    setOpenModal(true);
                }}
            >
                Add Funds
            </button>
            {openModal && (
                <AddFundsModal
                    onAddFunds={(amount) => {
                        deposit(amount).then(({ data, status }) => {
                            enqueueSnackbar(data.message, {
                                variant: status === 200 ? "success" : "error",
                            });
                            fetchUser();
                        });
                    }}
                    onClose={() => setOpenModal(false)}
                />
            )}
        </div>
    );
}

export default Funds;
