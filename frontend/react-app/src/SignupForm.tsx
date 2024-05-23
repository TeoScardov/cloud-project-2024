import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Input } from "./components/ui/input";
import { Button } from "./components/ui/button";
import axios from "axios";
import { useToast } from "./components/ui/use-toast";
import { useBackend } from "./services/backendService";

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

const formSchema = z.object({
    name: z.string().min(2, {
        message: "Name must be at least 2 characters.",
    }),
    surname: z.string().min(2, {
        message: "Surname must be at least 2 characters.",
    }),
    email_address: z.string().email({
        message: "Invalid email address.",
    }),
    username: z.string().min(2, {
        message: "Username must be at least 2 characters.",
    }),
    password: z.string().min(2, {
        message: "Password must be at least 2 characters.",
    }),
});

interface SignUpProps {
    onSubmit: (formData: z.infer<typeof formSchema>) => void;
}

const SignupForm: React.FC<any> = () => {
    const [credentialError, setCredentialError] = useState<string | null>(null);
    const [backendError, setBackendError] = useState<string | null>(null);

    // const backend = useBackend();
    const navigate = useNavigate();
    const { toast } = useToast();
    const backend = useBackend();

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            name: "",
            surname: "",
            email_address: "",
            username: "",
            password: "",
        },
    });

    const onSubmitHandler = async (formData: z.infer<typeof formSchema>) => {
        try {

            backend.postSignup(formData.name, formData.surname, formData.email_address, formData.username, formData.password).then((response: any) => {
                console.log(response);
                if (response) {
                    toast({
                        title: "Account created successfully!",
                        description: "You can now log in.",
                    });
                    navigate("/login");
                } else {
                    setCredentialError("Invalid credentials");
                }
            });
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

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmitHandler)} className="space-y-8">
                <div className="grid grid-cols-2 gap-4">
                    <div className="grid gap-2">
                        <FormField
                            control={form.control}
                            name="name"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Name</FormLabel>
                                    <FormControl>
                                        <Input
                                            placeholder="Nyquist"
                                            {...field}
                                        />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />
                    </div>
                    <div className="grid gap-2">
                        <FormField
                            control={form.control}
                            name="surname"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Surname</FormLabel>
                                    <FormControl>
                                        <Input placeholder="Gatto" {...field} />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />
                    </div>
                </div>
                <FormField
                    control={form.control}
                    name="email_address"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Email</FormLabel>
                            <FormControl>
                                <Input
                                    placeholder="nyquist@cat.miao"
                                    {...field}
                                />
                            </FormControl>

                            <FormMessage />
                        </FormItem>
                    )}
                />
                <FormField
                    control={form.control}
                    name="username"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Username</FormLabel>
                            <FormControl>
                                <Input placeholder="nyquist" {...field} />
                            </FormControl>

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
};

export default SignupForm;
