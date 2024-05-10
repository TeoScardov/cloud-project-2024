import { useState } from "react";
import reactLogo from "./assets/react.svg";

import Navbar from "./Navbar";
import BookCard from "./BookCard";
import Login from "./Login";
import { BackendProvider } from "./services/backendService";

function App() {
    const [count, setCount] = useState(0);

    return (
        <>
            <Navbar />
            <div className="flex justify-center items-center">
            <BookCard title="Title1" description="ciao1" price={10}/>
            <BookCard title="Title2" description="ciao2" price={20}/>
            <BookCard title="Title3" description="ciao3" price={30}/>
            <BookCard title="Title4" description="ciao4" price={40}/>
            <BookCard title="Title5" description="ciao5" price={50}/>
            </div>
           
        </>
    );
}

export default App;
