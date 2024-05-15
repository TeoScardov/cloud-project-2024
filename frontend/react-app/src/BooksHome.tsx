import BookCard from "./BookCard";

function BooksHome() {

    return (
        <div className="flex justify-center items-center">
            <BookCard title="Title1" description="ciao1" price={10}/>
            <BookCard title="Title2" description="ciao2" price={20}/>
            <BookCard title="Title3" description="ciao3" price={30}/>
            <BookCard title="Title4" description="ciao4" price={40}/>
            <BookCard title="Title5" description="ciao5" price={50}/>
            </div>
    );
}

export default BooksHome;