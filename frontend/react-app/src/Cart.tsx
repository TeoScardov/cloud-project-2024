import {
    Sheet,
    SheetContent,
    SheetDescription,
    SheetHeader,
    SheetTitle,
    SheetTrigger,
    SheetFooter,
    SheetClose
} from "./components/ui/sheet";

import { Suspense } from "react";

import { Button } from "./components/ui/button"
import { DataTable } from "./cart_items/data-table"
import { useState, useEffect } from 'react';

import { columns } from './cart_items/columns';
import CartItems from "./cart_items/page";

function Cart() {

    return (
      <Sheet>
        <SheetTrigger asChild>
          <Button variant="ghost">Cart</Button>
        </SheetTrigger>
        <SheetContent>
          <SheetHeader>
            <SheetTitle>Cart</SheetTitle>
            <SheetDescription>
              Make changes to your profile here. Click save when you're done.
            </SheetDescription>
          </SheetHeader>
          <Suspense fallback={<div>Loading...</div>}>
            <CartItems />
          </Suspense>
          <SheetFooter>
            <SheetClose asChild>
              <Button variant="outline_destructive">Clear Cart</Button>
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
