import BookCard from "./BookCard";
import { ScrollArea, ScrollBar } from "./components/ui/scroll-area";

function BooksHome() {
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
        <ScrollArea className="h-100vh w-100ow whitespace-nowrap rounded-md border">
            <div className="flex w-max space-x-10 p-4">
                <BookCard title="Title1" description="ciao1" price={10} />
                <BookCard title="Title2" description="ciao2" price={20} />
                <BookCard title="Title3" description="ciao3" price={30} />
                <BookCard title="Title4" description="ciao4" price={40} />
                <BookCard title="Title5" description="ciao5" price={50} />
                <BookCard title="Title1" description="ciao1" price={10} />
                <BookCard title="Title2" description="ciao2" price={20} />
                <BookCard title="Title3" description="ciao3" price={30} />
                <BookCard title="Title4" description="ciao4" price={40} />
                <BookCard title="Title5" description="ciao5" price={50} />
            </div>
            <ScrollBar orientation="horizontal" />
        </ScrollArea>

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
