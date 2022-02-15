import { useState } from "react";

interface Props {
    onAddFunds: (amount: number) => void;
    onClose: () => void;
}

function AddFundsModal({ onAddFunds, onClose }: Props) {
    const [amount, setAmount] = useState<number>(0);
    return (
        <div
            className="py-12 transition duration-150 ease-in-out z-20 absolute top-0 right-0 bottom-0 left-0"
            id="modal"
        >
            <div
                role="alert"
                className="container mx-auto w-11/12 md:w-2/3 max-w-lg"
            >
                <div className="relative py-8 px-5 md:px-10 bg-indigo-900 shadow-md rounded-xl border-2 border-white">
                    <h1 className="text-white font-lg font-bold tracking-normal leading-tight mb-4">
                        Add funds
                    </h1>
                    <div className="flex justify-center items-start flex-col">
                        <label
                            htmlFor="amount"
                            className="text-white text-sm font-bold leading-tight tracking-normal"
                        >
                            Amount
                        </label>
                        <select
                            className="bg-indigo-900 my-4"
                            id="amount"
                            onChange={(e) => {
                                setAmount(Number(e.target.value));
                            }}
                        >
                            <option value={5}>5</option>
                            <option value={10}>10</option>
                            <option value={20}>20</option>
                            <option value={50}>50</option>
                            <option value={100}>100</option>
                        </select>
                    </div>
                    <div className="flex items-center justify-start w-full mt-4">
                        <button
                            onClick={() => onAddFunds(amount)}
                            className="focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-700 transition duration-150 ease-in-out hover:bg-indigo-600 bg-indigo-700 rounded text-white px-8 py-2 text-sm"
                        >
                            Submit
                        </button>
                        <button
                            onClick={() => onClose()}
                            className="focus:outline-none focus:ring-2 focus:ring-offset-2  focus:ring-gray-400 ml-3 bg-gray-100 transition duration-150 text-gray-600 ease-in-out hover:border-gray-400 hover:bg-gray-300 border rounded px-8 py-2 text-sm"
                        >
                            Cancel
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default AddFundsModal;
