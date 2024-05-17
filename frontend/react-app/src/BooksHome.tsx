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

function BooksHome() {
    const [bookList, setBookList] = useState<Array<Book>>([]);

    useEffect(() => {
        fetch("http://0.0.0.0:4004/api/product/get-books")
            .then((response) => response.json())
            .then((data) => {
                setBookList(data);
            });
    }, []);

    return (
        // <ScrollArea className="h-100vh w-[350px] rounded-md border p-4">
        //     <div className="flex justify-center items-center">
        //         <BookCard title="Title1" description="ciao1" price={10} />
        //         <BookCard title="Title2" description="ciao2" price={20} />
        //         <BookCard title="Title3" description="ciao3" price={30} />
        //         <BookCard title="Title4" description="ciao4" price={40} />
        //         <BookCard title="Title5" description="ciao5" price={50} />
        //     </div>
        // </ScrollArea>

        // 50% on small screens and 33% on larger screens.
        <div className="flex min-h-screen w-full flex-col">
            <main className="flex min-h-[calc(100vh_-_theme(spacing.16))] flex-1 flex-col gap-4 bg-muted/40 p-4 md:gap-8 md:p-10">
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
                                        <BookCard
                                            key={book.isbn}
                                            title={book.title}
                                            description={book.description}
                                            price={book.price}
                                            product_id={book.isbn}
                                            isbn={book.isbn}
                                        />
                                    </div>
                                </CarouselItem>
                            ))}
                        </CarouselContent>
                        <CarouselNext />
                    </Carousel>
                </div>
            </main>
        </div>

        // <ScrollArea className="h-100vh w-100ow whitespace-nowrap rounded-md border">
        //     <div className="flex w-max space-x-10 p-4">
        //         <BookCard title="Title1" description="ciao1" price={10} />
        //         <BookCard title="Title2" description="ciao2" price={20} />
        //         <BookCard title="Title3" description="ciao3" price={30} />
        //         <BookCard title="Title4" description="ciao4" price={40} />
        //         <BookCard title="Title5" description="ciao5" price={50} />
        //         <BookCard title="Title1" description="ciao1" price={10} />
        //         <BookCard title="Title2" description="ciao2" price={20} />
        //         <BookCard title="Title3" description="ciao3" price={30} />
        //         <BookCard title="Title4" description="ciao4" price={40} />
        //         <BookCard title="Title5" description="ciao5" price={50} />
        //     </div>
        //     <ScrollBar orientation="horizontal" />
        // </ScrollArea>

        //     <ScrollArea className="w-96 whitespace-nowrap rounded-md border">
        //     <div className="flex w-max space-x-4 p-4">
        //       {works.map((artwork) => (
        //         <figure key={artwork.artist} className="shrink-0">
        //           <div className="overflow-hidden rounded-md">
        //             <Image
        //               src={artwork.art}
        //               alt={`Photo by ${artwork.artist}`}
        //               className="aspect-[3/4] h-fit w-fit object-cover"
        //               width={300}
        //               height={400}
        //             />
        //           </div>
        //           <figcaption className="pt-2 text-xs text-muted-foreground">
        //             Photo by{" "}
        //             <span className="font-semibold text-foreground">
        //               {artwork.artist}
        //             </span>
        //           </figcaption>
        //         </figure>
        //       ))}
        //     </div>
        //     <ScrollBar orientation="horizontal" />
        //   </ScrollArea>
    );
}

export default BooksHome;
