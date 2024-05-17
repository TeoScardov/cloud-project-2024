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

    const { toast } = useToast()

    const [token, setToken] = useState<string | null>(null);
    let [credentialError, setCredentialError] = useState<string | null>(null);
    let [backendError, setBackendError] = useState<string | null>(null);


    let navigate = useNavigate();

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            username: "",
            password: "",
        },
    });
    
    const onSubmitHandler = async (formData: z.infer<typeof formSchema>) => {
        try {
            // Validate form data against the schema
            console.log("Form data is valid:", JSON.stringify(formData));
            const responce = await axios.post(
                "http://127.0.0.1:4001/api/account/login",
                JSON.stringify(formData),
                {
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );
            console.log(responce);
            setToken(responce.data.access_token);
            localStorage.setItem("token", responce.data.access_token);
            toast({
                title: responce.data.message,
                //description: "You can view your cart by clicking the cart icon in the top right corner.",
              })
            navigate("/");
            
            // Optionally, you can redirect the user or show a success message
        } catch (error: any) {
            if (error instanceof z.ZodError) {
                console.error("Validation failed:", error.errors);
                setCredentialError("Invalid credentials");    
                // Optionally, you can handle validation errors, show error messages, etc.
            } else {
                console.error("Error submitting form:", error);
                setBackendError(error.response.data.message);
                // Optionally, you can handle other types of errors
            }
        }
    };

    // // 2. Define a submit handler.
    // function onSubmit(values: z.infer<typeof formSchema>) {
    //     setCredentialError(null);

    //     try {
    //         backend
    //             .loginAPI(values.username, values.username, values.password)
    //             .then(([token, message]) => {
    //                 setToken(token);
    //                 setMessage(message);
    //             });
    //     } catch (error) {
    //         console.error(error);
    //     }

    //     if (token) {
    //         localStorage.setItem("token", token);
    //     } else {
    //         setCredentialError("Invalid credentials");
    //     }

    //     if (token) {
    //         navigate("/");
    //     }
    // }


    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmitHandler)} className="space-y-8">
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
            {backendError ? <AlertError message = {backendError}/> : null}
            {credentialError ? <AlertError message = {credentialError}/> : null}
        </Form>
    );
}

/*
 {credentialError ? <AlertLogin/> : null}
*/

export default LoginForm;
