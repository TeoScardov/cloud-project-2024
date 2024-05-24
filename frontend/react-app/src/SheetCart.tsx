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
import { ShoppingCart } from "lucide-react";
import Cart from "./Cart";
import { useBackend } from "./services/backendService";
import { useNavigate } from "react-router-dom";
import CartItems from "./CartItems";

function SheetCart() {

    return (
        <Sheet>
            <SheetTrigger asChild>
                <Button variant="ghost">
                    <ShoppingCart size={24} />
                </Button>
            </SheetTrigger>
            <Cart />
        </Sheet>
    );
}

export default SheetCart;
