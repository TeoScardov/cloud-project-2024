import { useState } from "react";
import reactLogo from "./assets/react.svg";

import Navbar from "./Navbar";
import BookCard from "./BookCard";
import Login from "./Login";
import Signup from "./Signup";
import BooksHome from "./BooksHome";
// import { BackendProvider } from "./services/backendService";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Toaster } from "./components/ui/toaster";
import Profile from "./Profile";
import { ThemeProvider } from "./ThemeProvider";


function App() {

    return (
        // <BackendProvider>
            <BrowserRouter>
            <ThemeProvider>
                <Navbar />
                <Routes>
                    <Route path="/" element={<BooksHome />} />
                    <Route path="/login" element={ <Login/> } />
                    <Route path="/signup" element={ <Signup />} />
                    <Route path="/profile" element={ <Profile />} />
                </Routes>
                <Toaster />
            </ThemeProvider>
            </BrowserRouter>
        // </BackendProvider>
    );
}

export default App;
