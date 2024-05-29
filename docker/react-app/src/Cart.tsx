import { Button } from "./components/ui/button";
import {
    SheetContent,
    SheetHeader,
    SheetTitle,
    SheetFooter,
    SheetClose,
} from "./components/ui/sheet";
import CartItems from "./CartItems";
import { useNavigate } from "react-router-dom";
import { useBackend } from "./services/backendService";
import { useEffect, useState } from "react";
import { ScrollArea } from "@radix-ui/react-scroll-area";
import { set } from "react-hook-form";

function Cart() {
    const navigate = useNavigate();
    const backend = useBackend();
    const [isCartIdSet, setIsCartIdSet] = useState(false);
    const [isCartEmpty, setIsCartEmpty] = useState(true);

    const updateCartIdState = (value: boolean) => {
        setIsCartIdSet(value);
    };

    const updateCartEmptyState = (value: boolean) => {
        setIsCartEmpty(value);
    };

    const clearCart = async () => {
        backend.deleteCart();
        backend.getCartItems();
    };

    //console.log(isCartIdSet, !isCartEmpty);

    return (
        <SheetContent>
            <SheetHeader>
                <SheetTitle>Cart</SheetTitle>
            </SheetHeader>
                <CartItems
                    updateCartIdState={updateCartIdState}
                    updateCartEmptyState={updateCartEmptyState}
                />
            {isCartIdSet && !isCartEmpty ? (
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
                        <Button
                            type="submit"
                            onClick={() => navigate("/checkout")}
                        >
                            Checkout
                        </Button>
                    </SheetClose>
                </SheetFooter>
            ) : (
                <SheetFooter>
                    <SheetClose asChild>
                        <Button
                            variant="outline_destructive"
                            onClick={clearCart}
                            disabled
                        >
                            Clear Cart
                        </Button>
                    </SheetClose>
                    <div className="flex-grow" />
                    <SheetClose asChild>
                        <Button
                            type="submit"
                            onClick={() => navigate("/checkout")}
                            disabled
                        >
                            Checkout
                        </Button>
                    </SheetClose>
                </SheetFooter>
            )}
        </SheetContent>
    );
}

export default Cart;
