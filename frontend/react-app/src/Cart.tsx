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
import { DataTable } from "./cart_items/data-table";
import { useState, useEffect } from "react";

import { columns } from "./cart_items/columns";
import CartItems from "./cart_items/page";

function Cart() {
    return (
        <Sheet>
            <SheetTrigger asChild>
                <Button variant="ghost">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="16"
                        height="16"
                        fill="currentColor"
                        className="bi bi-bag-fill"
                        viewBox="0 0 16 16"
                    >
                        <path d="M8 1a2.5 2.5 0 0 1 2.5 2.5V4h-5v-.5A2.5 2.5 0 0 1 8 1m3.5 3v-.5a3.5 3.5 0 1 0-7 0V4H1v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V4z" />
                    </svg>
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
