import { Book, columns } from "./TableCartBook";
import { DataTable } from "./TableCartData";
import { Suspense, useEffect, useState } from "react";
// import { useBackend } from "../services/backendService";
import { Skeleton } from "./components/ui/skeleton";

export default function CartItems() {
    const [data, setData] = useState<Book[]>([]);
    let cart_books = useState<Book[] | null>(null)[0];

    const getData = async () => {

        let cart_id = "2eb1b208-c65d-4125-9c08-354d0c3b9a4c";

        if (cart_books) {
            return cart_books;
        }

        var responce = await fetch(`http://0.0.0.0:4005/api/cart/show_cart?cart_id=${cart_id}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        }
        );
        var json = await responce.json();

        console.log(json);

        json = JSON.parse(json.body);

        console.log(json);

        cart_books = json["items"];

        return cart_books!;
    };

    useEffect(() => {
        
        getData().then((data) => {
            setData(data);
        });

    }, []);

    return <DataTable columns={columns} data={data} />;
}
