import LibraryCard from "./LibraryCard";
import { Book } from "./TableCartBook";
import { Card, CardContent, CardHeader, CardTitle } from "./components/ui/card";

function Library(props: { library: Array<Book["isbn"]> }) {
    const library = props.library;

    return (
        <Card x-chunk="dashboard-04-chunk-1">
            <CardHeader>
                <CardTitle>Library</CardTitle>
            </CardHeader>
            <CardContent>
                {library.length === 0 ? (
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
                        No eBooks available
                    </div>
                ) : (
                        <div
                            style={{
                                display: "grid",
                                gridTemplateColumns:
                                    "repeat(auto-fill, minmax(200px, 1fr))",
                                gap: "1rem",
                                overflow: "auto",
                                maxHeight: "600px",
                                padding: "1rem",
                                borderRadius: "10px",
                                //boxShadow: "0 0 10px rgba(0,0,0,0.1)",
                            }}
                        >
                            {library.map((data, index) => (
                                <div key={index}>
                                    <LibraryCard isbn={data} />
                                </div>
                            ))}
                        </div>
                )}
            </CardContent>
        </Card>
    );
}

export default Library;
