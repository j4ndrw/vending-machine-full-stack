import { ChangeEvent } from "react";

interface Props {
    onChange: (e: ChangeEvent<HTMLSelectElement>) => void;
}

function SelectRole({ onChange }: Props) {
    return (
        <div className="flex justify-center items-center flex-col">
            <label htmlFor="role">Select role</label>
            <select
                id="role"
                className="m-4 p-2 text-xl flex justify-center items-center flex-col bg-purple-900"
                onChange={onChange}
            >
                <option value="buyer">Buyer</option>
                <option value="seller">Seller</option>
            </select>
        </div>
    );
}

export default SelectRole;
