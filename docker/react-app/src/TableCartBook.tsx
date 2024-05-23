import { ColumnDef } from "@tanstack/react-table"
 
export type Book = {
  isbn: string
  title: string
  name: string
  price: number
  description: string
  image_url: string
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
]