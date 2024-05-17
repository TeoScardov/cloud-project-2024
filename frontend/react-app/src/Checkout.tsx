import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "./components/ui/card";
import { Button } from "./components/ui/button";
import { Separator } from "./components/ui/separator";
import {
    ChevronLeft,
    ChevronRight,
    Copy,
    CreditCard,
    MoreVertical,
    Truck,
} from "lucide-react";
import { HandCoins } from "lucide-react";
import { useState, useEffect } from "react";
import axios from "axios";
import { Cookies } from "react-cookie";
import { set } from "react-hook-form";
import { PersonInformation } from "./EditInformationForm";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { Book } from "./TableCartBook";

function Checkout() {
    const [books, setBooks] = useState<Book[]>([]);
    const [cart_id, setCartId] = useState(null);
    const [total, setTotal] = useState(0);
    const [personalInfo, setPersonalInfo] = useState<PersonInformation>({
        name: "",
        surname: "",
        username: "",
        email_address: "",
        phone_number: "",
        billing_address: "",
        cc: "",
        expiredate: "",
        cvv: "",
    });

    const cookies = new Cookies();
    const navigate = useNavigate();

    useEffect(() => {
        if (!cookies.get("cart_id")) {
            console.log("No cart_id found");
        } else {
            setCartId(cookies.get("cart_id"));
        }

        fetchBooks(cookies.get("cart_id"));

        fetchPersonalInfo();
    }, []);

    const fetchBooks = async (cart_id: any) => {
        const responce = await axios.get(
            `http://0.0.0.0:4005/api/cart/show_cart?cart_id=${cart_id}`,
            {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            }
        );

        console.log(responce.data.body);

        const json = await JSON.parse(responce.data.body);

        console.log(json);

        const cart_books = json["items"];

        if (cart_books === null) {
            setBooks([]);
            setTotal(0);
        } else {
            setBooks(cart_books);
            setTotal(json["total"]);
        }
    };

    const fetchPersonalInfo = async () => {
        try {
            const response = await axios.post(
                "http://127.0.0.1:4001/api/account/info",
                {},
                {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + localStorage.getItem("token"),
                    },
                }
            );

            console.log(response);

            setPersonalInfo(response.data);

        } catch (error: any) {
            console.error("Error:", error);
        }
    }
            

    return (
        <div
            style={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                padding: "50px",
            }}
        >
            <Card className="overflow-hidden" x-chunk="dashboard-05-chunk-4">
                <CardHeader className="flex flex-row items-start bg-muted/50">
                    <div className="grid gap-0.5">
                        <CardTitle className="group flex items-center gap-2 text-lg">
                            Your Order
                        </CardTitle>
                        <CardDescription>
                            Date: {new Date().toLocaleDateString()}
                        </CardDescription>
                    </div>
                </CardHeader>
                <CardContent className="p-6 text-sm">
                    <div className="grid gap-3">
                        <div className="font-semibold">Order Details</div>
                        <ul className="grid gap-3">
                            {books.map((book, index) => (
                                <li
                                    key={index}
                                    className="flex items-center justify-between"
                                >
                                    <span className="text-muted-foreground">
                                        {book.name}
                                    </span>
                                    <span>${book.price.toFixed(2)}</span>
                                </li>
                            ))}
                        </ul>
                        <Separator className="my-2" />
                        <ul className="grid gap-3">
                            <li className="flex items-center justify-between font-semibold">
                                <span className="text-muted-foreground">
                                    Total
                                </span>
                                <span>${total}</span>
                            </li>
                        </ul>
                    </div>
                    <Separator className="my-4" />
                    <div className="grid grid-cols-2 gap-4">
                        <div className="grid gap-3">
                            <div className="font-semibold">
                                Billing Information
                            </div>
                            <address className="grid gap-0.5 not-italic text-muted-foreground">
                                {personalInfo.billing_address}
                            </address>
                        </div>
                    </div>
                    <Separator className="my-4" />
                    <div className="grid gap-3">
                        <div className="font-semibold">
                            Customer Information
                        </div>
                        <dl className="grid gap-3">
                            <div className="flex items-center justify-between">
                                <dt className="text-muted-foreground">
                                    Customer
                                </dt>
                                <dd>{personalInfo.name} {personalInfo.surname}</dd>
                            </div>
                            <div className="flex items-center justify-between">
                                <dt className="text-muted-foreground">Email</dt>
                                <dd>
                                    <a href="mailto:">{personalInfo.email_address}</a>
                                </dd>
                            </div>
                            <div className="flex items-center justify-between">
                                <dt className="text-muted-foreground">Phone</dt>
                                <dd>
                                    <a href="tel:">{personalInfo.phone_number}</a>
                                </dd>
                            </div>
                        </dl>
                    </div>
                    <Separator className="my-4" />
                    <div className="grid gap-3">
                        <div className="font-semibold">Payment Information</div>
                        <dl className="grid gap-3">
                            <div className="flex items-center justify-between">
                                <dt className="flex items-center gap-1 text-muted-foreground">
                                    <CreditCard className="h-4 w-4" />
                                </dt>
                                {!personalInfo.cc ? (
                                    <Link to="/profile">
                                        Add Payment Method
                                    </Link>
                                 ) : (
                                    <dd>{"*".repeat(personalInfo.cc.slice(0,-4).length) + personalInfo.cc.slice(-4)}</dd>
                                )}
                            </div>
                        </dl>
                    </div>
                </CardContent>
                <CardFooter className="flex flex-row items-center border-t bg-muted/50 px-6 py-3 justify-end">
                    <Button size="sm" variant="outline" className="h-8 gap-1">
                        <span className="lg:sr-only xl:not-sr-only xl:whitespace-nowrap">
                            Pay
                        </span>
                        <HandCoins size={24} />
                    </Button>
                </CardFooter>
            </Card>
        </div>
    );
}

export default Checkout;
