import BookCard from "./BookCard";
import { ScrollArea, ScrollBar } from "./components/ui/scroll-area";
import {
    Carousel,
    CarouselContent,
    CarouselItem,
    CarouselNext,
    CarouselPrevious,
} from "./components/ui/carousel";
import { useEffect, useState } from "react";
import { Book } from "./TableCartBook";
import { useBackend } from "./services/backendService";

function BooksHome() {
    const [bookList, setBookList] = useState<Array<Book>>([]);

    const backend = useBackend();

    useEffect(() => {

        backend.getHomeBooks(backend.numberOfBooksToDisplay).then((response: any) => {
            if (response === null) {
                throw new Error("No response");
            }
            setBookList(response);
        });
            
    }, []);

    return (
        <div className="flex min-h-screen w-full flex-col">
                <div
                    style={{
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center",
                        height: "60vh",
                    }}
                >
                    <Carousel
                        opts={{
                            align: "start",
                        }}
                        className="w-[100%] max-w-[80%]"
                    >
                        <CarouselPrevious />
                        <CarouselContent className="-ml-1">
                            {bookList.map((book) => (
                                <CarouselItem
                                    className="md:basis-1/2 lg:basis-1/4"
                                    key={book.isbn}
                                >
                                    <div className="p-1" key={book.isbn}>
                                        <BookCard {...book} />
                                    </div>
                                </CarouselItem>
                            ))}
                        </CarouselContent>
                        <CarouselNext />
                    </Carousel>
                </div>
        </div>
    );
}

export default BooksHome;
