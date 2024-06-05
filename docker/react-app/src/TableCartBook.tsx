import { ColumnDef } from "@tanstack/react-table"
 
export type Book = {
  isbn: string
  title: string
  price: number
  description: string
  image_url: string
}
 
export const columns: ColumnDef<Book>[] = [
  {
    accessorKey: "title",
    header: "Title",
  },
  {
    accessorKey: "price",
    header: "Price",
  },
]