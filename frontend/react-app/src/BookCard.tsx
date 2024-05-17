import { Button } from "./components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "./components/ui/card";
import { Input } from "./components/ui/input";
import { Label } from "./components/ui/label";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "./components/ui/select";

import "./BookCard.css"
import { useToast } from "./components/ui/use-toast"
import { Book } from "./TableCartBook";
import Cookies from 'universal-cookie';

function BookCard(props: Book) {

    const { toast } = useToast()
    const cookies = new Cookies();

    const handleClick = async () => {


        let cart_id = null

        if (localStorage.getItem("cart_id")) {

            cart_id = localStorage.getItem("cart_id")
        }

        try {
            let response = await fetch('http://0.0.0.0:4005/api/cart/addProduct', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    product_id: props.isbn,
                    cart_id: cart_id
                }),
            });

            console.log(response)
            const cookie = response.headers.get('Set-Cookie')
            console.log(cookie)
            //cookies.set("cart_id", cookie., { path: '/' });
            //console.log(cookies.get('myCat')); // Pacman
    
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
    
            const data = await response.json();

            console.log(data);
    
            toast({
                title: props.title + " added to cart!",
                //description: "You can view your cart by clicking the cart icon in the top right corner.",
            });
    
            console.log('Button clicked!');
            // You can add any other logic you need here
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <Card className="card">
            <CardHeader>
                <img src="https://placehold.co/150x150/png" alt="Book cover" />
            </CardHeader>
            <CardContent>
                <div>
                    <CardTitle className="text-xl">{props.title}</CardTitle>
                    {/* <CardDescription>
                        {props.description}
                    </CardDescription> */}
                </div>
                <div className="grid gap-4">
                </div>    

                <div>
                    <Label htmlFor="price">Price</Label>
                    <CardDescription>${props.price}</CardDescription>
                </div>
               
            </CardContent>
            <div className="flex justify-center"/>
            <CardFooter className="flex justify-between">
                <Button className="card_button" variant="outline">Details</Button>
                <Button className="card_button" onClick={handleClick}>Add to Cart</Button>
            </CardFooter>
        </Card>
    );
}

export default BookCard;
