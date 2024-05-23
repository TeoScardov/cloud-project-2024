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
import axios from "axios";
import { Book } from "./TableCartBook";
import { useBackend } from "./services/backendService";
import { useNavigate } from "react-router-dom";
import Information from "./Information";
import { PersonInformation } from "./EditInformationForm";
import { set } from "react-hook-form";
import Orders from "./Orders";

function Profile() {
    const [showLibrary, setShowLibrary] = useState<Boolean>(false);
    const [showOrders, setShowOrders] = useState<Boolean>(false);
    const [personalInformation, setPersonalInformation] =useState<PersonInformation>();
    const [library, setLibrary] = useState<Array<Book["isbn"]>>([]);

    const backend = useBackend();
    const navigate = useNavigate();

    useEffect(() => {
        
        if (localStorage.getItem("token") !== null) {
            backend.getAuth().then((response: any) => {
                if (response.status !== 200) {
                    navigate("/login");
                }
            });
        }

        backend.getPersonalInfo().then((response: any) => {

            if (response === null) {
                window.location.href = "/login";
            }
            console.log(response);
            setPersonalInformation(response);
            setLibrary(response.library);
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
                            <Link onClick={() => {setShowLibrary(false), setShowOrders(false)}} to="#">
                                {" "}
                                Information{" "}
                            </Link>
                        </ul>
                        <ul className="flex flex-col gap-2">
                            <Link onClick={() => {setShowLibrary(true), setShowOrders(false)}} to="#">
                                {" "}
                                Library{" "}
                            </Link>
                        </ul>
                        <ul className="flex flex-col gap-2">
                            <Link onClick={() => {setShowOrders(true), setShowLibrary(false)}} to="#">
                                {" "}
                                Orders{" "}
                            </Link>
                        </ul>
                    </nav>
                    <div className="grid gap-6">
                        {showLibrary ? (
                            <Card x-chunk="dashboard-04-chunk-1">
                                <Library library={library}/>
                            </Card>
                        ) : (

                            showOrders ? (
                                <Orders />
                            ) : (

                            <Card x-chunk="dashboard-04-chunk-2">
                                <CardHeader>
                                    <CardTitle>Personal Information</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <Information/>
                                </CardContent>
                                <CardFooter className="border-t px-6 py-4">
                                    <EditInformation/>
                                </CardFooter>
                            </Card>
                        ))}
                    </div>
                </div>
            </main>
        </div>
    );
}

export default Profile;
