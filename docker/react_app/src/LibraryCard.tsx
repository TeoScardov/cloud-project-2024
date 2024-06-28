import { Button } from "./components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "./components/ui/card";

import { Label } from "./components/ui/label";
import { useToast } from "./components/ui/use-toast";
import { Book } from "./TableCartBook";
import { useBackend } from "./services/backendService";
import { useEffect, useState } from "react";

function LibraryCard(props:{isbn: Book["isbn"]}) {

    const { toast } = useToast();
    const backend = useBackend();
    const [bookData, setBookData] = useState<Book>({
        name: "",
        title: "",
        isbn: "",
        price: 0,
        image_url: "",
        description: "",
    });
    const isbn = props.isbn;

    useEffect(() => {
        backend.getBookByIsbn(isbn).then((data: any) => {
            setBookData(data.book);
        }
        );
    }, []);

    return (
<Card className="w-full h-full overflow-hidden shadow-lg rounded-lg">
    <CardHeader>
        <img
            src={bookData.image_url}
            alt="Book cover"
            style={{ maxWidth: "200px", maxHeight: "250px", objectFit: "cover" }}
            className="w-full h-64"
        />
    </CardHeader>
    <CardContent className="h-32 overflow-auto p-4">
        <div>
            <CardTitle className="text-xl line-clamp-2 overflow-hidden font-semibold">
                {bookData.title}
            </CardTitle>
            <CardDescription className="text-gray-700 mt-2">
                {bookData.description}
            </CardDescription>
        </div>
    </CardContent>

    <CardFooter className="flex justify-between p-4 bg-muted/40 rounded-b-lg">
        <Button className="card_button" variant="outline">
            Read
        </Button>
    </CardFooter>
</Card>
    );
}

export default LibraryCard;
