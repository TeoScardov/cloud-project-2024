import { Scroll } from "lucide-react";
import LibraryCard from "./LibraryCard";
import { Book } from "./TableCartBook";
import { ScrollArea } from "@radix-ui/react-scroll-area";

function Library(props: { library: Array<Book["isbn"]> }) {
    const library = props.library;

    return library.length === 0 ? (
        <div
            style={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                height: "60vh",
                fontSize: "1.5em",
                color: "#888",
            }}
        >
            e No books available
        </div>
    ) : (
        <div style={{ overflowY: "auto", maxHeight: "500px" }}>
            <ScrollArea>
            <div
                style={{
                    display: "grid",
                    gridTemplateColumns:
                        "repeat(auto-fill, minmax(200px, 1fr))",
                    gap: "1rem",
                }}
            >
                {library.map((data, index) => (
                    <div key={index}>
                        <LibraryCard isbn={data} />
                    </div>
                ))}
            </div>
            </ScrollArea>
        </div>

    );
}

export default Library;
