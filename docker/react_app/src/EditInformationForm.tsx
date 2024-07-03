import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Input } from "./components/ui/input";
import { Button } from "./components/ui/button";
import { useToast } from "./components/ui/use-toast";
import { useBackend } from "./services/backendService";

import {
    Form,
    FormControl,
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
    phone_number: z.string().optional(),
    billing_address: z.string().optional(),
    cc: z.string().optional(),
    expiredate: z.string().optional(),
    cvv: z.string().optional(),
    password: z.string().optional(),
    account_id: z.any().optional(),
});

interface PersonInformation {
    name: string;
    surname: string;
    username: string;
    email_address: string;
}

interface CustomerInformation extends PersonInformation {
    phone_number: string;
    billing_address: string;
    cc: string;
    expiredate: string;
    cvv: string;
}

interface ModifyInformation extends CustomerInformation {
    account_id: string | undefined;
    password?: string | undefined;
}



interface ModifyInformationFormProps {
    onSubmit: (formData: z.infer<typeof formSchema>) => void;
}

const EditInformationForm: React.FC<any> = (props: ModifyInformation) => {
    const [credentialError, setCredentialError] = useState<string | null>(null);
    const [backendError, setBackendError] = useState<string | null>(null);
    const [accountId, setAccountId] = useState<string | null>(null);

    // const backend = useBackend();
    let navigate = useNavigate();
    const { toast } = useToast();
    const backend = useBackend();

    useEffect(() => {
        if (!localStorage.getItem("token")) {
            navigate("/login");
        }

        backend.getAuth().then((response: any) => {
            if (response === null) {
                navigate("/login");
            }
            setAccountId(response.data.account_id);
        });
    }, []);

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            name: props.name || "",
            surname: props.surname || "",
            username: props.username || "",
            email_address: props.email_address || "",
            phone_number: props.phone_number || "",
            billing_address: props.billing_address || "",
            cc: props.cc || "",
            expiredate: props.expiredate || "",
            cvv: props.cvv || "",
            password: undefined || "",
            account_id: props.account_id || "",
        },
    });

    const onSubmitHandler = async (formData: z.infer<typeof formSchema>) => {
        try {
            console.log(accountId);
            formData.account_id = accountId; //type: ignore

            if (formData.password == null || formData.password == "") {
                delete formData.password;
            }

            // Validate form data against the schema
            console.log("Form data is valid:", JSON.stringify(formData));
            
            backend.postUpdateInfo(formData).then((response: any) => {
                console.log(response);
                toast({
                    title: "Information updated successfully!",
                    //description: "You can now log in.",
                });
                window.location.reload();

            });

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
                                        <Input
                                            placeholder="MM/YY"
                                            {...field}
                                            type="cc-exp"
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
                                            type="cc-csc"
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
export type { PersonInformation, CustomerInformation, ModifyInformation, ModifyInformationFormProps};
