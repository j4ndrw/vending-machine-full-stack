import useUser from "../hooks/useUser";
import AppBar from "./AppBar";
import Buy from "./Buy";
import Sell from "./Sell";

function VendingMachine() {
    const { role } = useUser();

    return (
        <div>
            <AppBar />
            <div className="pt-48">{role === "buyer" ? <Buy /> : <Sell />}</div>
        </div>
    );
}

export default VendingMachine;
