import {
    Sheet,
    SheetTrigger,
} from "./components/ui/sheet";

import { Button } from "./components/ui/button";
import { ShoppingCart } from "lucide-react";
import Cart from "./Cart";

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
