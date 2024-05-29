import { Book, columns } from "./TableCartBook";
import { DataTable } from "./TableCartBookData";
import { Suspense, useEffect, useState } from "react";
import { Card } from "./components/ui/card";
import { useBackend } from "./services/backendService";

export default function CartItems(props:{updateCartIdState: (arg0: boolean) => void, updateCartEmptyState: (arg0: boolean) => void}) {
    const [dataBook, setDataBook] = useState<Book[] | null>(null);
    const backend = useBackend();

    const updateCartIdState = props.updateCartIdState;
    const updateCartEmptyState = props.updateCartEmptyState;

    useEffect(() => {
        if (!localStorage.getItem("cart_id")) {
            console.log("No cart_id found");

            return;
        } else {
            //getData()
            backend.getCartItems().then((data: any) => {
                //console.log(data.items);
                setDataBook(data.items);
                updateCartIdState(true);

                // if (data.items.length === 0 || data.items === null) {
                if (data.items === null) {
                    updateCartEmptyState(true);
                } else {
                    updateCartEmptyState(false);
                }
            });
        }
    }, []);

    const handleClickDelete = (isbn: string) => {
        backend.deleteCartItem(isbn).then(() => {
            backend.getCartItems().then((data: any) => {
                setDataBook(data.items);

                // if (data.items.length === 0) {
                if (data.items === null) {
                    updateCartEmptyState(true);
                } else {
                    updateCartEmptyState(false);
                }
            });
        });
    };

    return (
        <div>
            {!localStorage.getItem("cart_id") || dataBook === null ? (
    <Card>
        <div
            style={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                height: "60vh",
                fontSize: "1.5em",
                color: "#888",
            }}
        >
            Empty cart
        </div>
    </Card>
) : (
        <div  className="overflow-auto max-h-[500px]" >
        <DataTable
            columns={columns}
            data={dataBook}
            handleClickDelete={handleClickDelete}
        />
    </div>
)}
        </div>
    );
}
