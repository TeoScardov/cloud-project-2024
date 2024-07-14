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
import cat404 from "../public/404.png"; // Tell webpack this JS file uses this image

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
                        {/* all other routes */}
                        <Route
                            path="*"
                            element={<div
                                style={{
                                  display: "flex",
                                  flexDirection: "column",
                                  alignItems: "center",
                                  justifyContent: "center",
                                  height: "100vh",
                                }}
                              >
                                <h1
                                  style={{
                                    fontSize: "3rem",
                                    color: "#333",
                                    marginBottom: "20px",
                                  }}
                                >
                                  404 - Not Found
                                </h1>
                                <img src={cat404} alt="404" style={{ maxWidth: "50%", height: "auto" }} />
                              </div>
                            }
                        />
                    </Routes>
                </main>
                <Toaster />
            </ThemeProvider>
        </BrowserRouter>
    );
}

export default App;
