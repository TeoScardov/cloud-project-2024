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

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import AlertError from "./AlertError";

const formSchema = z.object({
    name: z.string().min(0, {
        message: "Name must be at least 2 characters.",
    }),
    surname: z.string().min(0, {
        message: "Surname must be at least 2 characters.",
    }),
    username: z.string().min(0, {
        message: "Username must be at least 2 characters.",
    }),
    email_address: z.string().email({
        message: "Invalid email address.",
    }),
    phone_number: z.string().min(0, {
        message: "Phone number must be at least 2 characters.",
    }),
    billing_address: z.string().min(0, {
        message: "Address must be at least 2 characters.",
    }),
    cc: z.string().min(0, {
        message: "Credit card must be at least 2 characters.",
    }),
    expiredate: z.string().min(0, {
        message: "Expire date must be at least 2 characters.",
    }),
    cvv: z.string().min(0, {
        message: "CVV must be at least 2 characters.",
    }),
    password: z.string().min(0, {
        message: "Password must be at least 2 characters.",
    }),
    account_id: z.any(),
});

interface PersonInformation {
    name?: string;
    surname?: string;
    username?: string;
    email_address?: string;
    phone_number?: string;
    billing_address?: string;
    cc: string;
    expiredate: string;
    cvv: string;
    password?: string;
    account_id?: string;
}

interface PersonInformationFormProps {
    onSubmit: (formData: z.infer<typeof formSchema>) => void;
}

const EditInformationForm: React.FC<any> = (props: PersonInformation) => {
    const [credentialError, setCredentialError] = useState<string | null>(null);
    const [backendError, setBackendError] = useState<string | null>(null);
    const [account_id, account_id_set] = useState<string | null>(null);

    // const backend = useBackend();
    let navigate = useNavigate();
    const { toast } = useToast();


    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.post(
                    "http://127.0.0.1:4001/api/account/authenticate",
                    {},
                    {
                        headers: {
                            "Content-Type": "application/json",
                            "Authorization": "Bearer " + localStorage.getItem("token"),
                        },
                    }
                );

                console.log(response);

                account_id_set(response.data.account_id);

                console.log(account_id);

            } catch (error: any) {
                if (error instanceof z.ZodError) {
                    console.error("Validation failed:", error.errors);
                    setCredentialError("Invalid credentials");
                } else {
                    console.error("Error submitting form:", error);
                    setBackendError(error.response?.data?.message || "Unknown error");
                }
            }
        };

        fetchData();
    }, []);

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            name: props.name,
            surname: props.surname,
            username: props.username,
            email_address: props.email_address,
            phone_number: props.phone_number,
            billing_address: props.billing_address,
            cc: props.cc,
            expiredate: props.expiredate,
            cvv: props.cvv,
            password: "",
            account_id: props.account_id,
        },
    });

    const onSubmitHandler = async (formData: z.infer<typeof formSchema>) => {
        
        try {

            console.log(account_id);
            formData.account_id = account_id; //type: ignore

            if (formData.password === "") {
                delete formData.password;
            }

            // Validate form data against the schema
            console.log("Form data is valid:", JSON.stringify(formData));
            const responce = await axios.post(
                "http://127.0.0.1:4001/api/account/update",
                JSON.stringify(formData),
                {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + localStorage.getItem("token"),
                    },
                }
            );
            console.log(responce);
            toast({
                title: "Information updated successfully!",
                //description: "You can now log in.",
            });
            window.location.reload();

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
                    name="billing_address"
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
                                        type="cc-number"
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
                                        <Input placeholder="MM/YY" {...field} type="cc-exp" />
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
                                        <Input placeholder="CVV" {...field} type="cc-csc" />
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
                                    placeholder="*************"
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
