import { Book, columns } from "./columns";
import { DataTable } from "./data-table";
import { Suspense, useEffect, useState } from "react";
import { useBackend } from "../services/backendService";
import { Skeleton } from "../components/ui/skeleton";

export default function CartItems() {
    const backend = useBackend();
    const [data, setData] = useState<Book[]>([]);

    useEffect(() => {
        backend.getData().then((data) => {
            setData(data);
        });
    }, []);

    return <DataTable columns={columns} data={data} />;
}
