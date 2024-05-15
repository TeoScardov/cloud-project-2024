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

function Profile() {

    const [library, setLibrary] = useState<Boolean>(false);

    useEffect(() => {
        if (!localStorage.getItem("token")) {
            window.location.href = "/login";
        }
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
                            <Link onClick={() => setLibrary(false)} to="#"> Information </Link>
                        </ul>
                        <ul className="flex flex-col gap-2">
                            <Link onClick={() => setLibrary(true)} to="#"> Library </Link>
                        </ul>
                    </nav>
                    <div className="grid gap-6">
                        {library ? (
                        <Card x-chunk="dashboard-04-chunk-1">
                            <CardHeader>
                                <CardTitle>Store Name</CardTitle>
                                <CardDescription>
                                    Used to identify your store in the
                                    marketplace.
                                </CardDescription>
                            </CardHeader>
                            <CardContent>
                                <form>
                                    <Input placeholder="Store Name" />
                                </form>
                            </CardContent>
                            <CardFooter className="border-t px-6 py-4">
                                <Button>Save</Button>
                            </CardFooter>
                        </Card>
                        ) : (
                        <Card x-chunk="dashboard-04-chunk-2">
                            <CardHeader>
                                <CardTitle>Plugins Directory</CardTitle>
                                <CardDescription>
                                    The directory within your project, in which
                                    your plugins are located.
                                </CardDescription>
                            </CardHeader>
                            <CardContent>
                                <form className="flex flex-col gap-4">
                                    <Input
                                        placeholder="Project Name"
                                        defaultValue="/content/plugins"
                                    />
                                    <div className="flex items-center space-x-2">
                                        <label
                                            htmlFor="include"
                                            className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                                        >
                                            Allow administrators to change the
                                            directory.
                                        </label>
                                    </div>
                                </form>
                            </CardContent>
                            <CardFooter className="border-t px-6 py-4">
                                <Button>Save</Button>
                            </CardFooter>
                        </Card> )}
                    </div>
                </div>
            </main>
        </div>
    );
}

export default Profile;
