import { useEffect, useState } from "react";
import { Book } from "../cart_items/columns";
import { createContext, useContext, ReactNode } from "react";
import { UserProfileToken } from "../auth/models";
import axios from "axios";

const api_account = "http://localhost:4001/api/account";

class BackendService {

    private cart_books: Book[] | null = null;
    private token: string | null = null;

    private static instance: BackendService | null = null;

    public static getInstance(): BackendService {
        if (!BackendService.instance) {
            BackendService.instance = new BackendService()
        }
        return BackendService.instance
    }

    public async getData(): Promise<Book[]> {
      
        if (this.cart_books) {
            return this.cart_books;
        }

        var responce = await fetch("http://127.0.0.1:9999");
        var json = await responce.json();

        this.cart_books = json["books"];

        return this.cart_books!;

    } 

}

export const useBackend = (): BackendService => {
    const backendService = useContext(BackendContext)
    if (!backendService) {
        throw new Error('useBackend must be used within a BackendProvider')
    }
    return backendService
}

interface BackendProviderProps {
    children: ReactNode;
}

export function BackendProvider ({ children }: BackendProviderProps) {
    const backendService = BackendService.getInstance()
    return (
        <BackendContext.Provider value={backendService}>
            {children}
        </BackendContext.Provider>
    )
}

const BackendContext = createContext<BackendService | null>(null);



