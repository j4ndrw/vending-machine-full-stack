import useSellerProducts from "../hooks/useSellerProducts";

import { DataGrid, GridColDef } from "@mui/x-data-grid";
import { useState } from "react";
import { buy } from "../services/buy";
import { useSnackbar } from "notistack";
import { fetchProductsFromUser, fetchUser } from "../store";
import AddProductModal from "./AddProductModal";
import { createProduct } from "../services/createProduct";

function Sell() {
    const { enqueueSnackbar } = useSnackbar();

    const { products } = useSellerProducts();

    const columns: GridColDef[] = [
        { field: "id", headerName: "ID", flex: 2 },
        { field: "amount_available", headerName: "Amount Available", flex: 2 },
        { field: "cost", headerName: "Cost", flex: 2 },
        { field: "product_name", headerName: "Name", flex: 2 },
        { field: "seller_id", headerName: "Seller", flex: 2 },
    ];

    const [openAddProductModal, setOpenAddProductModal] =
        useState<boolean>(false);

    return (
        <div className="flex justify-center items-center flex-col">
            {products.length === 0 ? (
                <h1>You haven't added any products to the Vending Machine</h1>
            ) : (
                <div>
                    <div
                        className="mt-10"
                        style={{ height: 300, width: "40vw" }}
                    >
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
                        />
                    </div>
                    <div className="flex justify-center items-center flex-col"></div>
                </div>
            )}
            <button
                className="mt-16 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-700 transition duration-150 ease-in-out hover:bg-blue-600 bg-blue-700 rounded text-white px-8 py-2 text-sm"
                onClick={() => {
                    setOpenAddProductModal(true);
                }}
            >
                Add product to Vending Machine
            </button>
            {openAddProductModal && (
                <AddProductModal
                    onAddProduct={(name, cost) => {
                        createProduct(cost, name).then(({ data, status }) => {
                            enqueueSnackbar(data.message, {
                                variant: status === 200 ? "success" : "error",
                            });
                            fetchProductsFromUser();
                        });
                    }}
                    onClose={() => setOpenAddProductModal(false)}
                />
            )}
        </div>
    );
}

export default Sell;
