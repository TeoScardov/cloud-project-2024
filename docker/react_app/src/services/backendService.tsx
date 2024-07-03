import { Book } from "../TableCartBook";
import { createContext, useContext, ReactNode } from "react";
import axios from "axios";
import {
    CustomerInformation,
} from "../EditInformationForm";

const API_ACCOUNT = process.env.ACCOUNT_SERVICE_URL + "/api/account";
const API_PURCHASE = process.env.PURCHASE_SERVICE_URL + "/api/purchase";
const API_PRODUCT = process.env.PRODUCT_CATALOG_URL + "/api/product";
const API_CART = process.env.SHOPPING_CART_URL + "/api/cart";
const NUMBER_OF_BOOKS_TO_DISPLAY = process.env.NUMBER_OF_BOOKS_TO_DISPLAY as unknown as number;
export interface AuthResponse {
    status: number;
    // add other properties if needed
}
class BackendService {
    private static instance: BackendService | null = null;

    public cart_books: Book[] | null = null;
    public cart_total: number | null = null;
    public token: string | null = null;
    public cart_id: string | null = null;
    public user_id: string | null = null;
    public credentialError: string | null = null;
    public backendError: string | null = null;
    public personalInfo: CustomerInformation | null = null;
    public numberOfBooksToDisplay: number = NUMBER_OF_BOOKS_TO_DISPLAY;

    public static getInstance(): BackendService {
        if (!BackendService.instance) {
            BackendService.instance = new BackendService();
        }
        return BackendService.instance;
    }

    public getCartItems: any = async () => {
        try {
            if (localStorage.getItem("cart_id")) {
                this.cart_id = localStorage.getItem("cart_id");

                const response = await axios.get(
                    `${API_CART}/show_cart?cart_id=${this.cart_id}`,
                    {
                        headers: {
                            "Content-Type": "application/json",
                        },
                    }
                );

                this.cart_books = response.data.items;
                this.cart_total = response.data.total;

                if (this.cart_books === null) {
                    this.cart_books = [];
                    this.cart_total = 0;
                }

                return response.data;
            } else {
                return null;
            }
        } catch (error) {
            console.error("An error occurred while fetching the cart:", error);
            return null;
        }
    };

    public deleteCartItem: any = async (isbn: any) => {
        console.log("Delete book with isbn", isbn);

        try {
            const response = await axios.delete(`${API_CART}/removeProduct`, {
                data: {
                    isbn: isbn,
                    cart_id: localStorage.getItem("cart_id"),
                },
            });

            console.log("Book deleted", response.data);
        } catch (error) {
            console.error("Error deleting book", error);
        }
    };

    public deleteCart: any = async () => {

        if (this.cart_id === null) {
            return;
        }

        try {
            const response = await axios.delete(`${API_CART}/removeCart`, {
                data: { cart_id: this.cart_id },
                headers: {
                    Authorization: "Bearer " + localStorage.getItem("token"),
                },
            });

            localStorage.removeItem("cart_id");
            this.cart_id = null;
            this.cart_books = null;
            this.cart_total = null;

            return response;
        } catch (error) {
            console.error("Error clearing cart", error);
        }
    };

    public postLogin: any = async (
        username: string,
        email: string,
        password: string
    ) => {
        try {
            const response = await axios.post(
                `${API_ACCOUNT}/login`,
                {
                    username: username,
                    email: email,
                    password: password,
                },
                {
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );

            if (response.status === 200) {
                this.token = response.data.access_token;

                localStorage.setItem("token", this.token!);

                return [this.token, response.data.message];
            } else {
                return [null, response.data.message];
            }
        } catch (error: any) {
            this.credentialError = error.response.data.message;
            return [null, this.credentialError];
        }
    };

    public postSignup: any = async (
        name: string,
        surname: string,
        email_address: string,
        username: string,
        password: string
    ) => {
        try {
            const response = await axios.post(
                `${API_ACCOUNT}/register`,
                {
                    name: name,
                    surname: surname,
                    email_address: email_address,
                    username: username,
                    password: password,
                },
                {
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );

            return response.data;
        } catch (error: any) {
            this.backendError = error.response.data.message;
            return this.backendError;
        }
    };

    public logOut: any = async () => {
        localStorage.removeItem("token");
        localStorage.removeItem("cart_id");

        this.cart_books = null;
        this.cart_total = null;
        this.token = null;
        this.cart_id = null;
        this.user_id = null;
        this.credentialError = null;
        this.backendError = null;
        this.personalInfo = null;


    };

    public getPersonalInfo: any = async () => {
        try {
            const response = await axios.post(
                `${API_ACCOUNT}/info`,
                {},
                {
                    headers: {
                        "Content-Type": "application/json",
                        Authorization:
                            "Bearer " + localStorage.getItem("token"),
                    },
                }
            );

            this.personalInfo = response.data;

            return response.data;
        } catch (error: any) {
            console.error("Error:", error);
            return null;
        }
    };

    public getAuth: any = async () => {
        try {
            const response = await axios.post(
                `${API_ACCOUNT}/authenticate`,
                {},
                {
                    headers: {
                        "Content-Type": "application/json",
                        Authorization:
                            "Bearer " + localStorage.getItem("token"),
                    },
                }
            );

            if (response.status === 200) {
                this.user_id = response.data.user_id;
                this.token = localStorage.getItem("token");
            }

            return response;
        } catch (error: any) {
            console.error("Error:", error);
            return null;
        }
    };

    public postAddProduct: any = async (isbn: any) => {
        if (localStorage.getItem("cart_id")) {
            this.cart_id = localStorage.getItem("cart_id");
        }

        try {
            const response = await axios.post(
                `${API_CART}/addProduct`,
                {
                    isbn: isbn,
                    cart_id: this.cart_id,
                },
                {
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );

            localStorage.setItem("cart_id", response.data.cart_id);

            return response.data;
        } catch (error: any) {
            console.error("Error:", error);
            return null;
        }
    };

    public getHomeBooks: any = async (number_of_books: number) => {
        const response = await axios.get(
            `${API_PRODUCT}/get-random-books/${number_of_books}`,
            {
                headers: {
                    "Content-Type": "application/json",
                },
            }
        );

        if (response.status !== 200) {
            return null;
        } else {
            return response.data;
        }
    };

    public postUpdateInfo: (info: any) => Promise<any> = async (info) => {
        try {
            const response = await axios.post(
                `${API_ACCOUNT}/update`,
                JSON.stringify(info),
                {
                    headers: {
                        "Content-Type": "application/json",
                        Authorization:
                            "Bearer " + localStorage.getItem("token"),
                    },
                }
            );

            return response.data;
        } catch (error: any) {
            console.error("Error:", error);
            return null;
        }
    };

    public postPurchase: any = async () => {
        try {
            if (this.personalInfo === null) {
                return null;
            }

            const response = await axios.post(
                `${API_PURCHASE}/`,
                {
                    cart: {
                        total: this.cart_total,
                    },
                },
                {
                    headers: {
                        "Content-Type": "application/json",
                        Authorization:
                            "Bearer " + localStorage.getItem("token"),
                    },
                }
            );

            return response;
        } catch (error: any) {
            console.error("Error:", error);
            return null;
        }
    };

    public postPayment: any = async (postPurchaseResponse: any) => {
        try {
            if (this.personalInfo === null) {
                return null;
            }

            const response = await axios.post(
                `${API_PURCHASE}/payment`,
                {
                    purchase: postPurchaseResponse.purchase,
                    billing_address: this.personalInfo.billing_address,
                    cc: this.personalInfo.cc,
                    expiredate: this.personalInfo.expiredate,
                    cvv: this.personalInfo.cvv,
                },
                {
                    headers: {
                        "Content-Type": "application/json",
                        Authorization:
                            "Bearer " + localStorage.getItem("token"),
                    },
                }
            );

            return response;
            
        } catch (error: any) {
            console.error("Error:", error);
            return null;
        }
    };

    public postAddBookToPurchase: any = async (postPurchaseResponse: any) => {
        try {
            const response = await axios.post(
                `${API_PURCHASE}/add-book-to-purchase`,
                {
                    cart: {
                        items: this.cart_books,
                    },
                    purchase: postPurchaseResponse.purchase,
                },
                {
                    headers: {
                        "Content-Type": "application/json",
                        Authorization:
                            "Bearer " + localStorage.getItem("token"),
                    },
                }
            );

            return response;
        } catch (error: any) {
            console.error("Error:", error);
            return null;
        }
    };

    public postAddBookToAccount: any = async (postPurchaseResponse: any) => {
        try {
            const response = await axios.post(
                `${API_PURCHASE}/add-book-to-account`,
                {
                    cart: {
                        items: this.cart_books,
                    },
                    purchase: postPurchaseResponse.purchase,
                },
                {
                    headers: {
                        "Content-Type": "application/json",
                        Authorization:
                            "Bearer " + localStorage.getItem("token"),
                    },
                }
            );

            return response;
        } catch (error: any) {
            console.error("Error:", error);
            return null;
        }
    };

    public getBookByIsbn: any = async (isbn: string) => {
        const response = await axios.post(
            `${API_PRODUCT}/get-book-details`,
            {
                isbn: isbn,
            },
            {
                headers: {
                    "Content-Type": "application/json",
                },
            }
        );

        return response.data;
    };

    public getOrders: any = async () => {
        try {
            const response = await axios.get(`${API_PURCHASE}/orders`, {
                headers: {
                    "Content-Type": "application/json",
                    Authorization: "Bearer " + localStorage.getItem("token"),
                },
            });

            return response.data;
        } catch (error: any) {
            console.error("Error:", error);
            return null;
        }
    };

    public putLinkCart = async () => {
        try {

            if (this.cart_id === null) {
                this.cart_id = localStorage.getItem("cart_id");
            }

            const response = await axios.put(
                `${API_CART}/link-cart`,
                {
                    cart_id: this.cart_id,
                },
                {
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: "Bearer " + localStorage.getItem("token"),
                    },
                }
            );

            return response.data;
        } catch (error: any) {
            console.error("Error:", error);
            return null;
        }
    }

    public getCart = async () => {

        try {
            const response = await axios.get(`${API_CART}/get_cart`, {
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + localStorage.getItem("token"), 
                },
            });

            console.log("Cart response", response.data);

            if (response.data.cart_id === null) {

                return null;

            } else {

                this.cart_id = response.data.cart_id;
                localStorage.setItem("cart_id", this.cart_id!);
            }

            return response.data;
        }
        catch (error: any) {
            console.error("Error:", error);
            return null;
        }
    }
}

export const useBackend = (): BackendService => {
    const backendService = useContext(BackendContext);
    if (!backendService) {
        throw new Error("useBackend must be used within a BackendProvider");
    }
    return backendService;
};

interface BackendProviderProps {
    children: ReactNode;
}

export function BackendProvider({ children }: BackendProviderProps) {
    const backendService = BackendService.getInstance();
    return (
        <BackendContext.Provider value={backendService}>
            {children}
        </BackendContext.Provider>
    );
}

const BackendContext = createContext<BackendService | null>(null);
