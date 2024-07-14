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
import { useState } from "react";

function Cart() {
    const navigate = useNavigate();
    const backend = useBackend();
    const [isCartIdSet, setIsCartIdSet] = useState(false);
    const [isCartEmpty, setIsCartEmpty] = useState(true);
    const isAuth = backend.token !== null;

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

    const onClickCheckout = () => {
        navigate("/checkout");
    }


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
                    {isAuth ? (
                        <SheetClose asChild>
                            <Button
                                variant="outline_destructive"
                                onClick={clearCart}
                            >
                                Clear Cart
                            </Button>
                        </SheetClose>
                    ) : null}
                    <div className="flex-grow" />
                    <SheetClose asChild>
                        <Button
                            type="submit"
                            onClick={onClickCheckout}
                        >
                            Checkout
                        </Button>
                    </SheetClose>
                </SheetFooter>
            ) : (
                <SheetFooter>
                    {isAuth ? (
                        <SheetClose asChild>
                            <Button
                                variant="outline_destructive"
                                onClick={clearCart}
                                disabled
                            >
                                Clear Cart
                            </Button>
                        </SheetClose>
                    ) : null}
                    <div className="flex-grow" />
                    <SheetClose asChild>
                        <Button
                            type="submit"
                            onClick={onClickCheckout}
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
