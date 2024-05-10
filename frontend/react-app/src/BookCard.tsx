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
import { ReactElement, JSXElementConstructor, ReactNode, ReactPortal } from "react";

function BookCard(props: { title: string; description: string; price: number; }) {
    return (
        <Card className="card">
            <CardHeader>
                <img src="https://via.placeholder.com/150" alt="Book cover" />
            </CardHeader>
            <CardContent>
                <div>
                    <CardTitle className="text-xl">{props.title}</CardTitle>
                    <CardDescription>
                        {props.description}
                    </CardDescription>
                </div>
                <div className="grid gap-4">
                </div>    

                <div>
                    <Label htmlFor="price">Price</Label>
                    <CardDescription>${props.price}</CardDescription>
                </div>
               
            </CardContent>
            <CardFooter className="flex justify-between">
                <Button className="card_button" variant="outline">Details</Button>
                <Button className="card_button">Add to Cart</Button>
            </CardFooter>
        </Card>
    );
}

export default BookCard;
