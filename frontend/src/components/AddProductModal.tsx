import { useState } from "react";

interface Props {
    onAddProduct: (name: string, cost: number) => void;
    onClose: () => void;
}

function AddProductModal({ onAddProduct, onClose }: Props) {
    const [cost, setCost] = useState<number>(0);
    const [name, setName] = useState<string>("");

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
                        Add product
                    </h1>
                    <div className="flex justify-center items-start flex-col">
                        <label
                            htmlFor="cost"
                            className="text-white text-sm font-bold leading-tight tracking-normal"
                        >
                            Cost
                        </label>
                        <input
                            id="cost"
                            className="text-gray-600 focus:outline-none focus:border focus:border-indigo-700 font-normal w-full h-10 flex items-center pl-16 text-sm border-gray-300 rounded border"
                            type="number"
                            placeholder="Your product's cost"
                            onChange={(e) => {
                                if (isNaN(Number(e.target.value))) {
                                    setCost(0);
                                } else {
                                    setCost(Number(e.target.value));
                                }
                            }}
                        />
                    </div>
                    <div className="flex justify-center items-start flex-col">
                        <label
                            htmlFor="name"
                            className="text-white text-sm font-bold leading-tight tracking-normal"
                        >
                            Name
                        </label>
                        <input
                            id="name"
                            className="text-gray-600 focus:outline-none focus:border focus:border-indigo-700 font-normal w-full h-10 flex items-center pl-16 text-sm border-gray-300 rounded border"
                            type="text"
                            placeholder="Your product's name"
                            onChange={(e) => {
                                setName(e.target.value);
                            }}
                        />
                    </div>
                    <div className="flex items-center justify-start w-full mt-4">
                        <button
                            onClick={() => onAddProduct(name, cost)}
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

export default AddProductModal;
