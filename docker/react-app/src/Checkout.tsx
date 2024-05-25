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
import { Loader } from "lucide-react";
import { useState, useEffect } from "react";
import axios from "axios";
import { set } from "react-hook-form";
import { CustomerInformation, PersonInformation } from "./EditInformationForm";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { Book } from "./TableCartBook";
import { useBackend } from "./services/backendService";
import AlertError from "./AlertError";
import { useToast } from "./components/ui/use-toast";

function Checkout() {
    const [books, setBooks] = useState<Book[]>([]);
    const [total, setTotal] = useState(0);
    const [disabledClick, setDisabledClick] = useState(false);
    const [missingInfo, setMissingInfo] = useState<string[]>([]);
    const [personalInfo, setPersonalInfo] = useState<CustomerInformation>({
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

    const navigate = useNavigate();
    const backend = useBackend();
    const { toast } = useToast();

    useEffect(() => {
        if (localStorage.getItem("token") !== null) {
            backend.getAuth().then((response: any) => {
                if (response.status !== 200) {
                    navigate("/login");
                }
            });

            backend.getCartItems().then((data: any) => {
                setBooks(data.items);
                setTotal(data.total);

                console.log(data);
            });

            backend.getPersonalInfo().then((data: any) => {
                setPersonalInfo(data);
                setMissingInfo([]);
                for (const [key, value] of Object.entries(data)) {
                    if (value === "" || value === null) {
                        setMissingInfo((prev) => [...prev, key]);
                    }
                }
            });
        } else {
            toast({
                title: "You need to log in first!",
                type: "foreground",
            });
            navigate("/login");
        }
    }, []);

    const handleClick = async () => {

        setDisabledClick(true);

        const postPurchaseResponse = await postPurchase();

        console.log("postPurchaseResponse",postPurchaseResponse);
        
        if (postPurchaseResponse) {

            const purchase_data = postPurchaseResponse.data;

            const postPaymentResponse = await postPayment(purchase_data);

            console.log("postPaymentResponse", postPaymentResponse);

            const postAddBookToPurchaseResponse = await postAddBookToPurchase(purchase_data);

            console.log("postAddBookToPurchaseResponse",postAddBookToPurchaseResponse);
                            
            const postAddBookToAccountResponse = await postAddBookToAccount(purchase_data);

            console.log("postAddBookToAccountResponse",postAddBookToAccountResponse);
                    
            const postDeleteCartResponse = await postDeleteCart();

            console.log("postDeleteCartResponse",postDeleteCartResponse);

            navigate("/profile");

        } else {
            setDisabledClick(false);
        }
    };

    const postPurchase = async () => {
        const response = await backend.postPurchase();
        if (response.status !== 200) {
            toast({
                title: "Error in creating the purchase!",
            });
            setDisabledClick(false);
            return;
        } else {
            toast({
                title: "Purchase created successful!",
            });

            return response;
        }
    }

    const postPayment = async (postPurchaseResponse: any) => {
        const response = await backend.postPayment(postPurchaseResponse);
        if (response.status !== 200) {
            toast({
                title: "Error in creating the payment!",
            });
            setDisabledClick(false);
            return;
        } else {
            toast({
                title: "Payment created successful!",
            });

            return response;
        }
    }

    const postAddBookToPurchase = async (postPurchaseResponse: any) => {
        const response = await backend.postAddBookToPurchase(postPurchaseResponse);
        if (response.status !== 200) {
            toast({
                title: "Error in adding the book to the purchase!",
            });
            setDisabledClick(false);
            return;
        } else {
            toast({
                title: "Book added to purchase!",
            });

            return response;
        }
    }

    const postAddBookToAccount = async (postPurchaseResponse: any) => {
        const response = await backend.postAddBookToAccount(postPurchaseResponse);
        if (response.status !== 200) {
            toast({
                title: "Error in adding the book to the account!",
            });
            setDisabledClick(false);
            return;
        } else {
            toast({
                title: "Book added to account!",
            });

            return response;
        }
    }

    const postDeleteCart = async () => {
        const response = await backend.deleteCart();
        if (response.status !== 200) {
            toast({
                title: "Error in deleting the cart!",
            });
            setDisabledClick(false);
            return;
        } else {
            toast({
                title: "Cart deleted successful!",
            });

            return response;
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
                                <span>${total.toFixed(2)}</span>
                            </li>
                        </ul>
                    </div>
                    <Separator className="my-4" />
                    <div className="grid grid-cols-2 gap-4">
                        <div className="grid gap-3">
                            <div className="font-semibold">
                                Billing Information
                            </div>
                            {missingInfo.includes("billing_address") ? (
                                <Link
                                    to="/profile"
                                    style={{
                                        color: "#007bff",
                                        fontWeight: "bold",
                                        textDecoration: "none",
                                    }}
                                >
                                    Add Billing Address
                                </Link>
                            ) : (
                                <address className="grid gap-0.5 not-italic text-muted-foreground">
                                    {personalInfo.billing_address}
                                </address>
                            )}
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
                                <dd>
                                    {personalInfo.name} {personalInfo.surname}
                                </dd>
                            </div>
                            <div className="flex items-center justify-between">
                                <dt className="text-muted-foreground">Email</dt>
                                <dd>
                                    <a href="mailto:">
                                        {personalInfo.email_address}
                                    </a>
                                </dd>
                            </div>
                            <div className="flex items-center justify-between">
                                <dt className="text-muted-foreground">Phone</dt>
                                {missingInfo.includes("phone_number") ? (
                                    <Link
                                        to="/profile"
                                        style={{
                                            color: "#007bff",
                                            fontWeight: "bold",
                                            textDecoration: "none",
                                        }}
                                    >
                                        Add Phone Number
                                    </Link>
                                ) : (
                                    <dd>
                                        <a href="tel:">
                                            {personalInfo.phone_number}
                                        </a>
                                    </dd>
                                )}
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
                                    <Link
                                        to="/profile"
                                        style={{
                                            color: "#007bff",
                                            fontWeight: "bold",
                                            textDecoration: "none",
                                        }}
                                    >
                                        Add Payment Method
                                    </Link>
                                ) : (
                                    <dd>
                                        {"*".repeat(
                                            personalInfo.cc.slice(0, -4).length
                                        ) + personalInfo.cc.slice(-4)}
                                    </dd>
                                )}
                            </div>
                        </dl>
                    </div>
                </CardContent>
                <CardFooter className="flex flex-row items-center border-t bg-muted/50 px-6 py-3 justify-end">
                    {disabledClick ? (
                        <span className="text-muted-foreground animate-spin-slow">
                            <Loader />
                        </span>
                    ) : null}
                    <Button
                        size="sm"
                        variant="outline"
                        className="h-8 gap-1"
                        onClick={handleClick}
                        disabled={missingInfo.length > 0 || disabledClick}
                    >
                        <span className="lg:sr-only xl:not-sr-only xl:whitespace-nowrap">
                            Pay
                        </span>
                        <HandCoins size={24} />
                    </Button>
                </CardFooter>
                {missingInfo.length > 0 ? (
                    <AlertError
                        message={
                            "Missing Information" +
                            ": " +
                            missingInfo.join(", ")
                        }
                    />
                ) : null}
            </Card>
        </div>
    );
}

export default Checkout;
