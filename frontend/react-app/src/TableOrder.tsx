import { ColumnDef } from "@tanstack/react-table";

export type Order = {
    id: string;
    order_date: string;
    status: string;
    total_price: number;
};

export const columns: ColumnDef<Order>[] = [
    {
        accessorKey: "id",
        header: "Order ID",
    },
    {
        accessorKey: "order_date",
        header: "Order Date",
    },
    {
        accessorKey: "status",
        header: "Status",
    },
    {
        accessorKey: "total_price",
        header: "Total Price",
    },
];
