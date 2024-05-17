import {
    Sheet,
    SheetContent,
    SheetDescription,
    SheetHeader,
    SheetTitle,
    SheetTrigger,
    SheetFooter,
    SheetClose,
} from "./components/ui/sheet";

import { useState, useEffect } from "react";

import { Button } from "./components/ui/button";
import CartItems from "./CartItems";
import { ShoppingCart } from "lucide-react";
import { Cookies } from "react-cookie";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Cart() {
    const [cart_id, setCartId] = useState<string | null>(null);
    const cookies = new Cookies();
    const navigate = useNavigate();

    useEffect(() => {
        if (!cookies.get("cart_id")) {
            console.log("No cart_id found");
        } else {
            setCartId(cookies.get("cart_id"));
        }
    }, []);

    const clearCart = async () => {
        if (cookies.get("cart_id")) {
            setCartId(cookies.get("cart_id"));
        }

        try {
            const response = await axios.delete(
                "http://0.0.0.0:4005/api/cart/removeCart",
                {
                    data: { cart_id: cart_id},
                    headers: {
                        Authorization:
                            "Bearer " + localStorage.getItem("token"),
                    },
                }
            );

            console.log("Cart cleared", response.data);
        } catch (error) {
            console.error("Error clearing cart", error);
        }
    };

    return (
        <Sheet>
            <SheetTrigger asChild>
                <Button variant="ghost">
                    <ShoppingCart size={24} />
                </Button>
            </SheetTrigger>
            <SheetContent>
                <SheetHeader>
                    <SheetTitle>Cart</SheetTitle>
                </SheetHeader>
                <CartItems />
                {cart_id ? (
                    <SheetFooter>
                        <SheetClose asChild>
                            <Button
                                variant="outline_destructive"
                                onClick={clearCart}
                            >
                                Clear Cart
                            </Button>
                        </SheetClose>
                        <div className="flex-grow" />
                        <SheetClose asChild>
                            <Button type="submit" onClick={() => navigate("/checkout")}>Checkout</Button>
                        </SheetClose>
                    </SheetFooter>
                ) : null}
            </SheetContent>
        </Sheet>
    );
}

export default Cart;
