import useProducts from "../hooks/useProducts";

import { DataGrid, GridRowsProp, GridColDef } from "@mui/x-data-grid";
import { useState } from "react";
import { buy } from "../services/buy";
import { useSnackbar } from "notistack";
import { fetchProducts, fetchUser } from "../store";

function Buy() {
    const { enqueueSnackbar } = useSnackbar();

    const { products } = useProducts();

    const [total, setTotal] = useState<number>(0);

    const columns: GridColDef[] = [
        { field: "id", headerName: "ID", flex: 2 },
        { field: "amount_available", headerName: "Amount Available", flex: 2 },
        { field: "cost", headerName: "Cost", flex: 2 },
        { field: "product_name", headerName: "Name", flex: 2 },
        { field: "seller_id", headerName: "Seller", flex: 2 },
    ];

    const [selectedIds, setSelectedIds] = useState<number[]>([]);

    if (products.length === 0)
        return <h1>Nothing on stock at the moment. Come back later.</h1>;

    return (
        <div className="flex justify-center items-center flex-col">
            <div className="mt-10" style={{ height: 300, width: "40vw" }}>
                <DataGrid
                    className="text-white bg-blue-200"
                    rows={[
                        ...products.map((product) => ({
                            ...product,
                            id: product.product_id,
                        })),
                    ]}
                    columns={columns}
                    checkboxSelection
                    disableSelectionOnClick
                    disableColumnSelector
                    onSelectionModelChange={(selectedIds) => {
                        setTotal(() => {
                            let total = 0;
                            selectedIds.forEach((id) => {
                                const product = products.find(
                                    (product) => product.product_id === id
                                );
                                if (product) total += product.cost;
                            });
                            return total;
                        });
                        setSelectedIds(selectedIds as number[]);
                    }}
                />
            </div>
            <div className="flex justify-center items-center flex-col">
                <h1 className="mt-8">Total: {total}</h1>
                <button
                    className="mt-16 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-700 transition duration-150 ease-in-out hover:bg-blue-600 bg-blue-700 rounded text-white px-8 py-2 text-sm"
                    onClick={() => {
                        buy(total, selectedIds).then(({ data, status }) => {
                            enqueueSnackbar(data.message, {
                                variant: status === 200 ? "success" : "error",
                            });
                            fetchProducts();
                            fetchUser();
                        });
                    }}
                >
                    Buy
                </button>
            </div>
        </div>
    );
}

export default Buy;
