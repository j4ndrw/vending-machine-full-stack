import { useSnackbar } from "notistack";
import { useSnapshot } from "valtio";
import { logout } from "../services/logout";
import { updateUserRole } from "../services/updateUserRole";
import { fetchUser, store } from "../store";
import { Role } from "../types/role";
import Funds from "./Funds";
import SelectRole from "./SelectRole";

function AppBar() {
    const { loggedIn } = useSnapshot(store);
    const { enqueueSnackbar } = useSnackbar();
    return (
        <div className="flex items-center justify-between p-4 w-screen bg-purple-600 fixed top-0 left-0">
            <div className="flex items-center">
                <div className="text-xl flex justify-between items-center w-screen px-20">
                    <h1 className="font-bold no-underline  hover:text-gray-600">
                        Vending Machine
                    </h1>
                    {loggedIn ? (
                        <div className="flex justify-center items-center flex-row">
                            <SelectRole
                                onChange={(e) => {
                                    updateUserRole(e.target.value as Role).then(
                                        () => {
                                            fetchUser();
                                        }
                                    );
                                }}
                            />
                            <Funds />
                            <button
                                className="focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-700 transition duration-150 ease-in-out hover:bg-purple-600 bg-purple-700 rounded text-white px-8 py-2 text-sm"
                                onClick={() => {
                                    logout().then(({ data, status }) => {
                                        enqueueSnackbar(data.message, {
                                            variant:
                                                status === 200
                                                    ? "success"
                                                    : "error",
                                        });
                                    });
                                }}
                            >
                                Log Out
                            </button>
                        </div>
                    ) : (
                        <></>
                    )}
                </div>
            </div>
            <nav className="hidden md:block space-x-6">{}</nav>
        </div>
    );
}

export default AppBar;
