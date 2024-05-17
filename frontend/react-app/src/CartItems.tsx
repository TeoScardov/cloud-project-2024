import { Book, columns } from "./TableCartBook";
import { DataTable } from "./TableCartData";
import { Suspense, useEffect, useState } from "react";
import { Card } from "./components/ui/card";
import { Cookies } from "react-cookie";
import axios from "axios";

export default function CartItems() {
    const [dataBook, setDataBook] = useState<Book[]>([]);
    let cart_books = useState<Book[]>([])[0];

    const cookies = new Cookies();

    const getData = async () => {

        let cart_id = null;

        if (cookies.get("cart_id")) {
            cart_id = cookies.get("cart_id");
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

        if (cart_books === null) {
            cart_books = [];
        }

        setDataBook(cart_books);
    };

    useEffect(() => {
        
        if (!cookies.get("cart_id")) {
            console.log("No cart_id found");

            return;
        } else {

        getData()

        }

    }, []);

    const handleClickDelete = async (product_id: any) => {
        const cookies = new Cookies();
        
        console.log("Delete book with isbn", product_id)

        try {
          const response = await axios.delete(`http://0.0.0.0:4005/api/cart/removeProduct`, { data: { product_id: product_id, cart_id: cookies.get("cart_id")} });

          console.log("Book deleted", response.data);

            getData()

      } catch (error) {
          console.error("Error deleting book", error);
      }
      }


    return (
        <div>
            {!cookies.get("cart_id") || dataBook.length===0 ? (
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
                <DataTable columns={columns} data={dataBook} handleClickDelete={handleClickDelete}/>
            )}
        </div>
    );

}