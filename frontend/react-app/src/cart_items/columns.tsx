import { ColumnDef } from "@tanstack/react-table"
import { Button } from "../components/ui/button"
 
// This type is used to define the shape of our data.
// You can use a Zod schema here if you want.
export type Book = {
  name: string
  price: number
}
 
export const columns: ColumnDef<Book>[] = [
  {
    accessorKey: "name",
    header: "Name",
  },
  {
    accessorKey: "price",
    header: "Price",
  },
  {
    id: "actions",
    cell: ({ row }) => {
        return (
            <Button variant="secondary">🗑️</Button>
        )
    }
}
]