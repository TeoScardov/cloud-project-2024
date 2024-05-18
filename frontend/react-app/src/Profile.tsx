import { useEffect } from "react";
import { Link } from "react-router-dom";
import { Separator } from "./components/ui/separator";
import { Button } from "./components/ui/button";
import {
    Card,
    CardContent,
    CardFooter,
    CardHeader,
    CardTitle,
    CardDescription,
} from "./components/ui/card";
import { Input } from "./components/ui/input";
import { useState } from "react";
import Library from "./Library";
import EditInformation from "./EditInformation";
import Information, { PersonInformation } from "./Information";
import axios from "axios";
import { Book } from "./TableCartBook";

// const personalInformation: PersonInformation = {
//     name: "John",
//     surname: "Doe",
//     username: "johndoe",
//     email: "hohn.doe@ymail.com",
//     phone: "343663738",
//     address: "1234 Main St",
//     cc: "1234 5678 9012 3456",
//     expiredate: "12/27",
//     cvv: "123"
// };

function Profile() {
    const [showLibrary, setShowLibrary] = useState<Boolean>(false);
    const [personalInformation, setPersonalInformation] =useState<PersonInformation>();
    const [library, setLibrary] = useState<Array<Book>>([]);

    useEffect(() => {
        if (!localStorage.getItem("token")) {
            window.location.href = "/login";
        }

        const token = localStorage.getItem("token");

        axios
            .post(
                "http://127.0.0.1:4001/api/account/info",
                {},
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            )
            .then((response) => {
                setPersonalInformation(response.data);
                setLibrary(response.data.library);
                console.log(response.data);
                console.log(response.data.library);
            })
            .catch((error) => {
                console.error("Error:", error);
            });
    }, []);

    return (
        <div className="flex min-h-screen w-full flex-col">
            <main className="flex min-h-[calc(100vh_-_theme(spacing.16))] flex-1 flex-col gap-4 bg-muted/40 p-4 md:gap-8 md:p-10">
                <div className="mx-auto grid w-full max-w-6xl gap-2">
                    <h1 className="text-3xl font-semibold">Profile</h1>
                </div>

                <div className="mx-auto grid w-full max-w-6xl items-start gap-6 md:grid-cols-[180px_1fr] lg:grid-cols-[250px_1fr]">
                    <nav
                        className="grid gap-4 text-sm text-muted-foreground"
                        x-chunk="dashboard-04-chunk-0"
                    >
                        <ul className="flex flex-col gap-2">
                            <Link onClick={() => setShowLibrary(false)} to="#">
                                {" "}
                                Information{" "}
                            </Link>
                        </ul>
                        <ul className="flex flex-col gap-2">
                            <Link onClick={() => setShowLibrary(true)} to="#">
                                {" "}
                                Library{" "}
                            </Link>
                        </ul>
                    </nav>
                    <div className="grid gap-6">
                        {showLibrary ? (
                            <Card x-chunk="dashboard-04-chunk-1">
                                <Library library={library} />
                            </Card>
                        ) : (
                            <Card x-chunk="dashboard-04-chunk-2">
                                <CardHeader>
                                    <CardTitle>Personal Information</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <Information
                                        name={personalInformation?.name ?? ""}
                                        surname={
                                            personalInformation?.surname ?? ""
                                        }
                                        username={
                                            personalInformation?.username ?? ""
                                        }
                                        email_address={
                                            personalInformation?.email_address ??
                                            ""
                                        }
                                        phone_number={personalInformation?.phone_number ?? ""}
                                        billing_address={
                                            personalInformation?.billing_address ??
                                            ""
                                        }
                                        cc={personalInformation?.cc ?? ""}
                                        expiredate={
                                            personalInformation?.expiredate ??
                                            ""
                                        }
                                        cvv={personalInformation?.cvv ?? ""}
                                        password={personalInformation?.password ?? ""}
                                        account_id={personalInformation?.account_id ?? ""}

                                    />
                                </CardContent>
                                <CardFooter className="border-t px-6 py-4">
                                    <EditInformation
                                        name={personalInformation?.name ?? ""}
                                        surname={
                                            personalInformation?.surname ?? ""
                                        }
                                        username={
                                            personalInformation?.username ?? ""
                                        }
                                        email_address={personalInformation?.email_address ?? ""}
                                        phone_number={personalInformation?.phone_number ?? ""}
                                        billing_address={
                                            personalInformation?.billing_address ?? ""
                                        }
                                        cc={personalInformation?.cc ?? ""}
                                        expiredate={
                                            personalInformation?.expiredate ??
                                            ""
                                        }
                                        cvv={personalInformation?.cvv ?? ""}
                                        password={personalInformation?.password ?? ""}
                                        account_id={personalInformation?.account_id ?? ""}
                                    />
                                </CardFooter>
                            </Card>
                        )}
                    </div>
                </div>
            </main>
        </div>
    );
}

export default Profile;
