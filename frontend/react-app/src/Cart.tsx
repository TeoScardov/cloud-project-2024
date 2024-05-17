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

import { Suspense } from "react";

import { Button } from "./components/ui/button";
import { DataTable } from "./TableCartData";
import { useState, useEffect } from "react";

import { columns } from "./TableCartBook";
import CartItems from "./CartItems";
import { ShoppingCart} from "lucide-react";

function Cart() {
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
                    <SheetDescription>
                        Make changes to your profile here. Click save when
                        you're done.
                    </SheetDescription>
                </SheetHeader>
                <Suspense fallback={<div>Loading...</div>}>
                    <CartItems />
                </Suspense>
                <SheetFooter>
                    <SheetClose asChild>
                        <Button variant="outline_destructive">
                            Clear Cart
                        </Button>
                    </SheetClose>
                    <div className="flex-grow" />
                    <SheetClose asChild>
                        <Button type="submit">Checkout</Button>
                    </SheetClose>
                </SheetFooter>
            </SheetContent>
        </Sheet>
    );
}

export default Cart;
