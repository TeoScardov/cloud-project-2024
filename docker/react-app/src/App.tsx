import { useState } from "react";
import reactLogo from "./assets/react.svg";

import Navbar from "./Navbar";
import BookCard from "./BookCard";
import Login from "./Login";
import Signup from "./Signup";
import BooksHome from "./BooksHome";
import { BackendProvider } from "./services/backendService";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Toaster } from "./components/ui/toaster";
import Profile from "./Profile";
import { ThemeProvider } from "./ThemeProvider";
import Checkout from "./Checkout";


function App() {

    return (
        <BackendProvider>
            <BrowserRouter>
            <ThemeProvider>
            <Navbar />
                <main className="flex min-h-[calc(100vh_-_theme(spacing.16))] flex-1 flex-col gap-4 bg-muted/40 p-4 md:gap-8 md:p-10">
                <Routes>
                    <Route path="/" element={<BooksHome />} />
                    <Route path="/login" element={ <Login/> } />
                    <Route path="/signup" element={ <Signup />} />
                    <Route path="/profile" element={ <Profile />} />
                    <Route path="/checkout" element={ <Checkout />} />
                </Routes>
                </main>
                <Toaster />
            </ThemeProvider>
            </BrowserRouter>
         </BackendProvider>
    );
}

export default App;
