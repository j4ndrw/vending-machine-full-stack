import { readLoginStatus } from "./auth/loginStatus";
import Login from "./components/Login";
import Register from "./components/Register";
import VendingMachine from "./components/VendingMachine";

function App() {
    const isLoggedIn = readLoginStatus();

    return (
        <div className="flex justify-center items-center flex-col">
            {isLoggedIn ? (
                <VendingMachine />
            ) : (
                <div className="flex justify-center items-center">
                    <h1>Vending Machine</h1>
                    <Login />
                    <Register />
                </div>
            )}
        </div>
    );
}

export default App;
