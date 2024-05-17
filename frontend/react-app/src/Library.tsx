import BookCard from "./BookCard"; // Assumendo che BookCard sia un componente esistente
import { ScrollArea, ScrollBar } from "./components/ui/scroll-area";
import { Book } from "./TableCartBook";
interface LibraryProps {
    library: Array<Book>;
}

function Library(props: LibraryProps) {
    return props.library.length === 0 ? (
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
            No books available
        </div>
    ) : (
        <ScrollArea className="h-[60vh] w-[100%]">
            <ScrollBar>
                {props.library.map((book) => (
                    <BookCard
                        title={book.title}
                        description={book.description}
                        price={book.price}
                        isbn={book.isbn}
                    />
                ))}
            </ScrollBar>
        </ScrollArea>
    );
}

export default Library;
