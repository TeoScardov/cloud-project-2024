import { ColumnDef } from "@tanstack/react-table";

export type Order = {
    id: string;
    order_date: string;
    status: string;
    total: number;
};

export const columns: ColumnDef<Order>[] = [
    {
        id: "id",
        accessorKey: "id",
        header: "Order ID",
    },
    {
        id: "order_date",
        accessorKey: "order_date",
        header: "Order Date",
    },
    {
        id: "status",
        accessorKey: "status",
        header: "Status",
    },
    {
        id: "total",
        accessorKey: "total",
        header: "Total Price",
    },
];
