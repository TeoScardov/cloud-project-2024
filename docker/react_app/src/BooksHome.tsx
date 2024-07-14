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
import { set } from "react-hook-form";
import { Description } from "@radix-ui/react-dialog";

function BooksHome() {
    const [bookList, setBookList] = useState<Array<Book>>([]);
    const backend = useBackend();

    useEffect(() => {
        backend
            .getHomeBooks(backend.numberOfBooksToDisplay)
            .then((response: any) => {
                if (!response || !Array.isArray(response)) {
                    throw new Error("Invalid response format");
                } else {
                    setBookList(response);
                }
            })
            .catch((error: any) => {
                console.error("Error fetching books:", error);
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
                    {bookList.length > 0 ? (
                        <CarouselContent className="-ml-1">
                            {bookList.map((book) => (
                                <CarouselItem
                                    className="md:basis-1/2 lg:basis-1/4"
                                    key={book.isbn}
                                >
                                    <div className="p-1">
                                        <BookCard {...book} />
                                    </div>
                                </CarouselItem>
                            ))}
                        </CarouselContent>
                    ) : (
                        <div className="flex justify-center items-center w-full h-full">
                            <h1 className="text-2xl text-gray-600">
                                Loading books...
                            </h1>
                        </div>
                    )}
                    <CarouselNext />
                </Carousel>
            </div>
        </div>
    );
}

export default BooksHome;
