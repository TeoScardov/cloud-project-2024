import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Input } from "./components/ui/input";
import { Button } from "./components/ui/button";
import axios from "axios";
import { ReactElement, useEffect } from "react";

import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "./components/ui/form";

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import AlertError from "./AlertError";
import { useToast } from "./components/ui/use-toast";
import { useBackend } from "./services/backendService";

const formSchema = z.object({
    username: z.string().min(2, {
        message: "Username must be at least 2 characters.",
    }),
    password: z.string().min(2, {
        message: "Password must be at least 2 characters.",
    }),
});

interface LogInProps {
    onSubmit: (formData: z.infer<typeof formSchema>) => void;
}

const LoginForm: React.FC<any> = () => {
    const { toast } = useToast();
    const backend = useBackend();

    const [credentialError, setCredentialError] = useState<string | null>(null);
    const [backendError, setBackendError] = useState<string | null>(null);

    const navigate = useNavigate();

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            username: "",
            password: "",
        },
    });

    const onSubmitHandler = async (formData: z.infer<typeof formSchema>) => {

            backend
                .postLogin(
                    formData.username,
                    formData.username,
                    formData.password
                )
                .then(([token, message]:[string, string]) => {
                    if (token) {
                        localStorage.setItem("token", token);
                        navigate("/");
                    } else {
                        // Imposta l'errore delle credenziali se le credenziali non sono corrette
                        setCredentialError(message);
                    }
                }).catch((error: any) => {
                    console.error(error);
                    setBackendError("Errore durante l'accesso");
                });
            };

    return (
        <Form {...form}>
            <form
                onSubmit={form.handleSubmit(onSubmitHandler)}
                className="space-y-8"
            >
                <FormField
                    control={form.control}
                    name="username"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Username or Email</FormLabel>
                            <FormControl>
                                <Input placeholder="shadcn" {...field} />
                            </FormControl>
                            <FormDescription>
                                This is your public display name.
                            </FormDescription>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <FormField
                    control={form.control}
                    name="password"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Password</FormLabel>
                            <FormControl>
                                <Input
                                    placeholder=""
                                    type="password"
                                    {...field}
                                />
                            </FormControl>
                            <FormDescription>Your password</FormDescription>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <Button type="submit">Submit</Button>
            </form>
            {backendError ? <AlertError message={backendError} /> : null}
            {credentialError ? <AlertError message={credentialError} /> : null}
        </Form>
    );
};

/*
 {credentialError ? <AlertLogin/> : null}
*/

export default LoginForm;
