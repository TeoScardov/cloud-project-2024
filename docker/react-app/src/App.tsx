import Navbar from "./Navbar";
import Login from "./Login";
import Signup from "./Signup";
import BooksHome from "./BooksHome";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Toaster } from "./components/ui/toaster";
import Profile from "./Profile";
import { ThemeProvider } from "./ThemeProvider";
import Checkout from "./Checkout";
import { useBackend } from "./services/backendService";
import { useEffect } from "react";  

function App() {
    const backend = useBackend();

    useEffect(() => {
        if (localStorage.getItem("token") !== null) {
            backend.getAuth().then(() => {

                if (localStorage.getItem("cart_id") === null) {
                    backend.getCart();
                } else {
                    backend.putLinkCart();
                }
            });
        }
    }, []);

    return (
        <BrowserRouter>
            <ThemeProvider>
                <Navbar />
                <main className="flex min-h-[calc(100vh_-_theme(spacing.16))] flex-1 flex-col gap-4 bg-muted/40 p-4 md:gap-8 md:p-10">
                    <Routes>
                        <Route path="/" element={<BooksHome />} />
                        <Route path="/login" element={<Login />} />
                        <Route path="/signup" element={<Signup />} />
                        <Route path="/profile" element={<Profile />} />
                        <Route path="/checkout" element={<Checkout />} />
                    </Routes>
                </main>
                <Toaster />
            </ThemeProvider>
        </BrowserRouter>
    );
}

export default App;
