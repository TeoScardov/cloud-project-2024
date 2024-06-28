import {
    ColumnDef,
    flexRender,
    getCoreRowModel,
    useReactTable,
} from "@tanstack/react-table";

import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "./components/ui/table";

import { Skeleton } from "./components/ui/skeleton";

import { Button } from "./components/ui/button";
import { Trash2 } from "lucide-react";

interface BookDataTableProps<TData, TValue> {
    columns: ColumnDef<TData, TValue>[];
    data: TData[];
    handleClickDelete: (isbn: string) => void;
}

export function DataTable<TData, TValue>({
    columns,
    data,
    handleClickDelete,
}: BookDataTableProps<TData, TValue>) {
    const table = useReactTable({
        data,
        columns,
        getCoreRowModel: getCoreRowModel(),
    });

    return (
        <div className="rounded-md border">
            <Table>
                <TableHeader>
                    {table.getHeaderGroups().map((headerGroup) => (
                        <TableRow key={headerGroup.id}>
                            {headerGroup.headers.map((header) => {
                                return (
                                    <TableHead key={header.id}>
                                        {header.isPlaceholder
                                            ? null
                                            : flexRender(
                                                  header.column.columnDef
                                                      .header,
                                                  header.getContext()
                                              )}
                                    </TableHead>
                                );
                            })}
                        </TableRow>
                    ))}
                </TableHeader>
                <TableBody>
                    {table.getRowModel().rows?.length ? (
                        table.getRowModel().rows.map((row) => (
                            <TableRow
                                key={row.id}
                                data-state={row.getIsSelected() && "selected"}
                            >
                                {row.getVisibleCells().map((cell) => (
                                    <TableCell key={cell.id}>
                                        {flexRender(
                                            cell.column.columnDef.cell,
                                            cell.getContext()
                                        )}
                                    </TableCell>
                                ))}
                                <TableCell>
                                    <Button
                                        className="text-red-500"
                                        variant="ghost"
                                        onClick={() =>
                                            // @ts-ignore
                                            handleClickDelete(row.original.isbn)
                                        }
                                    >
                                        <Trash2 />
                                    </Button>
                                </TableCell>
                            </TableRow>
                        ))
                    ) : (
                        <Table>
                            <TableBody>
                                {[...Array(3)].map((_, index) => (
                                    <TableRow key={index}>
                                        <TableCell>
                                            <div className="flex items-center space-x-2">
                                                <div className="space-y-2">
                                                    <Skeleton className="h-4 w-[200px]" />
                                                    <Skeleton className="h-4 w-[150px]" />
                                                </div>
                                            </div>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    )}
                </TableBody>
            </Table>
        </div>
    );
}
