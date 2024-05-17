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
import { Cookies } from "react-cookie";

function BookCard(props: Book) {
    const { toast } = useToast();
    const cookies = new Cookies();

    const handleClickAdd = async () => {
        let cart_id: string | null = null;

        if (cookies.get("cart_id")) {
            cart_id = cookies.get("cart_id");
        }

        console.log(cart_id);

        try {
            let response = await fetch(
                "http://0.0.0.0:4005/api/cart/addProduct",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        product_id: props.isbn,
                        cart_id: cart_id,
                    }),
                }
            );

            //console.log(response)
            //const cookie = response.headers.get('Set-Cookie')
            //console.log(cookie)
            //cookies.set("cart_id", cookie., { path: '/' });
            //console.log(cookies.get('myCat')); // Pacman

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();

            console.log(data);

            const body = JSON.parse(data.body);

            cookies.set("cart_id", body.cart_id, { path: "/" });

            toast({
                title: props.title + " added to cart!",
                //description: "You can view your cart by clicking the cart icon in the top right corner.",
            });

            console.log("Button clicked!");
            // You can add any other logic you need here
        } catch (error) {
            console.error("Error:", error);
        }
    };

    return (
        <Card className="w-full h-full overflow-hidden">
            <CardHeader>
                <img src="https://placehold.co/150x150/png" alt="Book cover" />
            </CardHeader>
            <CardContent className="h-32 overflow-auto">
                <div>
                    <CardTitle className="text-xl line-clamp-2 overflow-hidden">
                        {props.title}
                    </CardTitle>
                    {/* <CardDescription>
                        {props.description}
                    </CardDescription> */}
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

            <CardFooter className="flex justify-between">
                <Button className="card_button" variant="outline">
                    Details
                </Button>
                <Button className="card_button" onClick={handleClickAdd}>
                    Add to Cart
                </Button>
            </CardFooter>
        </Card>
    );
}

export default BookCard;
