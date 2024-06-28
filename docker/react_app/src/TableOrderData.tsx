
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './components/ui/table';
import { Badge } from './components/ui/badge';
import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import { Skeleton } from './components/ui/skeleton';


interface OrderDataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
}

export function OrderTable<TData, TValue>({
  columns,
  data,
}: OrderDataTableProps<TData, TValue>) {

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
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
              <TableRow key={row.id}>
                {row.getVisibleCells().map((cell) =>
                  cell.column.columnDef.id === "status" ? (
                    <TableCell key={cell.id}>
                      <Badge variant="secondary">{flexRender(cell.column.columnDef.cell, cell.getContext())}</Badge>
                    </TableCell>
                  ) : (
                    <TableCell key={cell.id}>
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </TableCell>
                  )
                )}
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell>
                <div className="flex items-center space-x-2">
                  <div className="space-y-2">
                    <Skeleton className="h-4 w-[200px]" />
                  </div>
                </div>
              </TableCell>
            </TableRow>
          )}
        </TableBody>
    </Table>
  );

}

export default OrderTable;


