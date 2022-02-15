import { readLoginStatus } from "../auth/loginStatus";
import Funds from "./Funds";
import SelectRole from "./SelectRole";

function AppBar() {
    const isLoggedIn = readLoginStatus();
    return (
        <div className="flex items-center justify-between p-4 w-screen bg-purple-600 fixed top-0 left-0">
            <div className="flex items-center">
                <div className="text-xl flex justify-between items-center w-screen px-20">
                    <h1 className="font-bold no-underline  hover:text-gray-600">
                        Vending Machine
                    </h1>
                    {isLoggedIn ? (
                        <div className="flex justify-center items-center flex-row">
                            <SelectRole onChange={() => {}} />
                            <Funds />
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
