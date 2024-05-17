import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Input } from "./components/ui/input";
import { Button } from "./components/ui/button";
import axios from "axios";
import { useToast } from "./components/ui/use-toast";

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
    username: z.string().min(2, {
        message: "Username must be at least 2 characters.",
    }),
    email_address: z.string().email({
        message: "Invalid email address.",
    }),
    phone_number: z.string().min(2, {
        message: "Phone number must be at least 2 characters.",
    }),
    address: z.string().min(2, {
        message: "Address must be at least 2 characters.",
    }),
    cc: z.string().min(2, {
        message: "Credit card must be at least 2 characters.",
    }),
    expiredate: z.string().min(2, {
        message: "Expire date must be at least 2 characters.",
    }),
    cvv: z.string().min(2, {
        message: "CVV must be at least 2 characters.",
    }),
    password: z.string().min(2, {
        message: "Password must be at least 2 characters.",
    }),
});

interface PersonInformation {
    name: string;
    surname: string;
    username: string;
    email: string;
    phone: string;
    address: string;
    cc: string;
    expiredate: string;
    cvv: string;
}

interface PersonInformationFormProps {
    onSubmit: (formData: z.infer<typeof formSchema>) => void;
}

const EditInformationForm: React.FC<any> = (props: PersonInformation) => {
    let [credentialError, setCredentialError] = useState<string | null>(null);
    let [backendError, setBackendError] = useState<string | null>(null);

    // const backend = useBackend();
    let navigate = useNavigate();
    const { toast } = useToast();

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            name: props.name,
            surname: props.surname,
            username: props.username,
            email_address: props.email,
            phone_number: props.phone,
            address: props.address,
            cc: "",
            expiredate: "",
            cvv: "",
            password: "",
        },
    });

    const onSubmitHandler = async (formData: z.infer<typeof formSchema>) => {
        try {
            // Validate form data against the schema
            console.log("Form data is valid:", JSON.stringify(formData));
            const responce = await axios.post(
                "http://127.0.0.1:4001/api/account/register",
                JSON.stringify(formData),
                {
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );
            console.log(responce);
            toast({
                title: "Account created successfully!",
                description: "You can now log in.",
            });
            navigate("/");

            // Optionally, you can redirect the user or show a success message
        } catch (error: any) {
            if (error instanceof z.ZodError) {
                console.error("Validation failed:", error.errors);
                setCredentialError("Invalid credentials");
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
            <form
                onSubmit={form.handleSubmit(onSubmitHandler)}
                className="space-y-4"
            >
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
                    name="phone_number"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Phone Number</FormLabel>
                            <FormControl>
                                <Input placeholder="123-456-7890" {...field} />
                            </FormControl>

                            <FormMessage />
                        </FormItem>
                    )}
                />
                <FormField
                    control={form.control}
                    name="address"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Address</FormLabel>
                            <FormControl>
                                <Input
                                    placeholder="Av. Siempre Viva 123"
                                    {...field}
                                />
                            </FormControl>

                            <FormMessage />
                        </FormItem>
                    )}
                />
                <div className="col-span-3">
                    <FormField
                        control={form.control}
                        name="cc"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Credit Card</FormLabel>
                                <FormControl>
                                    <Input
                                        placeholder="Credit Card Number"
                                        {...field}
                                    />
                                </FormControl>

                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <div className="flex justify-between">
                        <FormField
                            control={form.control}
                            name="expiredate"
                            render={({ field }) => (
                                <FormItem>
                                    <FormControl>
                                        <Input
                                            placeholder="MM/YY"
                                            {...field}
                                        />
                                    </FormControl>

                                    <FormMessage />
                                </FormItem>
                            )}
                        />
                        <FormField
                            control={form.control}
                            name="cvv"
                            render={({ field }) => (
                                <FormItem>
                                    <FormControl>
                                        <Input
                                            placeholder="CVV"
                                            {...field}
                                        />
                                    </FormControl>

                                    <FormMessage />
                                </FormItem>
                            )}
                        />
                    </div>
                </div>
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
            {backendError ? <AlertError message={backendError} /> : null}
            {credentialError ? <AlertError message={credentialError} /> : null}
        </Form>
    );
};

export default EditInformationForm;
export type { PersonInformation };
