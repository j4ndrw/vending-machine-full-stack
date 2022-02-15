import { useSnapshot } from "valtio";
import Login from "./components/Login";
import Register from "./components/Register";
import VendingMachine from "./components/VendingMachine";
import { store } from "./store";

function App() {
    const { loggedIn } = useSnapshot(store);

    return (
        <div className="flex justify-center items-center flex-col">
            {loggedIn ? (
                <VendingMachine />
            ) : (
                <div className="flex justify-center items-center flex-col">
                    <h1>Vending Machine</h1>
                    <div className="flex justify-center items-center">
                        <Login />
                        <Register />
                    </div>
                </div>
            )}
        </div>
    );
}

export default App;
