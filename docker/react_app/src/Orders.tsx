import { useEffect, useState } from "react";
import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from "./components/ui/card";
import { Badge } from "./components/ui/badge";
import { OrderTable } from "./TableOrderData";
import { columns } from "./TableOrder";
import { useBackend } from "./services/backendService";

function Orders() {
    const [orders, setOrders] = useState<[]>([]);
    const [loaded, setLoaded] = useState<boolean>(false);
    const backend = useBackend();

    useEffect(() => {
        setLoaded(false);
        backend.getOrders().then((data: any) => {
            setOrders(data.purchase);
            setLoaded(true);
        });
    }, []);

    return (
        <Card x-chunk="dashboard-04-chunk-1">
            <CardHeader>
                <CardTitle>Orders</CardTitle>
            </CardHeader>
            <CardContent>
                {orders.length === 0 && loaded ? (
                    <div className="flex justify-center items-center h-64">
                        <Badge variant="secondary">No Orders</Badge>
                    </div>
                ) : (
                    <OrderTable columns={columns} data={orders} />
                )}
            </CardContent>
        </Card>
    );
}

export default Orders;
