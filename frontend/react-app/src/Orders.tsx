import React, { useEffect, useState } from "react";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "./components/ui/card";
import { Badge } from "./components/ui/badge";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "./components/ui/table";
import { OrderTable } from "./TableOrderData";
import { columns } from "./TableOrder";

function Orders() {
    const [orders, setOrders] = useState([]);

    useEffect(() => {
        const fetchOrders = async () => {
            const response = await fetch(
                "http://127.0.0.1:4003/api/purchase/orders",
                {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization:
                            "Bearer " + localStorage.getItem("token"),
                    },
                }
            );

            const orders = await response.json();
            setOrders(orders.purchase);
        };

        fetchOrders();
        console.log(orders);
    }, []);

    return (
        <Card x-chunk="dashboard-05-chunk-3">
            <CardHeader className="px-7">
                <CardTitle>Orders</CardTitle>
                <CardDescription>Recent orders.</CardDescription>
            </CardHeader>
            <CardContent>
                <OrderTable columns={columns} data={orders}/>
            </CardContent>
        </Card>
    );
}

export default Orders;
