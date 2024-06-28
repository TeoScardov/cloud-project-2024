import { Button } from "./components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "./components/ui/card";

import { Label } from "./components/ui/label";
import { useToast } from "./components/ui/use-toast";
import { Book } from "./TableCartBook";
import { useBackend } from "./services/backendService";
import { useEffect, useState } from "react";

function BookCard(props: Book) {
    const { toast } = useToast();
    const backend = useBackend();
    const [bookInCart, setBookInCart] = useState(false);
    const [bookInLibrary, setBookInLibrary] = useState(false);

    useEffect(() => {
        if (!localStorage.getItem("cart_id")) {
            return;
        } else {
            backend.getCartItems().then((data: any) => {
                if (data.items === null) {
                    return;
                } else {
                    data.items.forEach((item: any) => {
                        if (item.isbn === props.isbn) {
                            setBookInCart(true);
                        }
                    });
                }
            });
        }

        if (!localStorage.getItem("token")) {
            return;
        } else {
            backend.getPersonalInfo().then((response: any) => {
                if (response != null) {
                    response.library.forEach((item: any) => {
                        if (item === props.isbn) {
                            setBookInLibrary(true);
                        }
                    });
                }
            });
        }

        return () => {
            setBookInCart(false);
        };
    }, []);

    const handleClickAdd = async () => {
        try {
            await backend.postAddProduct(props.isbn);

            toast({
                title: props.title + " added to cart!",
                //description: "You can view your cart by clicking the cart icon in the top right corner.",
            });

            setBookInCart(true);
        } catch (error) {
            console.error("Error:", error);
        }
    };

    return (
        <Card
            className="w-full h-full overflow-hidden shadow-lg rounded-lg"
            style={{ maxWidth: "250px", maxHeight: "600px" }}
        >
            <CardHeader>
                <img
                    src={props.image_url}
                    alt="Book cover"
                    className="w-full h-64 object-cover"
                />
            </CardHeader>
            <CardContent className="h-32 overflow-auto p-4">
                <div>
                    <CardTitle className="text-xl line-clamp-2 overflow-hidden font-semibold">
                        {props.title}
                    </CardTitle>
                </div>

                <div className="justify-end mr-10">
                    <Label
                        htmlFor="price"
                        className="font-bold text-sm text-gray-500"
                    >
                        Price
                    </Label>
                    <CardDescription className="text-lg font-semibold">
                        ${props.price}
                    </CardDescription>
                </div>
            </CardContent>

            <CardFooter className="flex justify-between p-4 bg-muted/40 rounded-b-lg">
                <Button className="card_button" variant="outline">
                    Details
                </Button>
                {bookInCart ? (
                    <Button className="card_button" variant="outline" disabled>
                        In Cart
                    </Button>
                ) : bookInLibrary ? (
                    <Button className="card_button" variant="outline" disabled>
                        In Library
                    </Button>
                ) : (
                    <Button className="card_button" onClick={handleClickAdd}>
                        Add to Cart
                    </Button>
                )}
            </CardFooter>
        </Card>
    );
}

export default BookCard;
