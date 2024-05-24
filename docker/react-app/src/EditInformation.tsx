import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "./components/ui/dialog";

import { Button } from "./components/ui/button";
import { PersonInformation } from "./EditInformationForm";
import EditInformationForm from "./EditInformationForm";
import { useBackend } from "./services/backendService";
import { useEffect, useState } from "react";

function EditInformation() {

    const [personalInformation, setPersonalInformation] = useState<PersonInformation | null>(null);

    const backend = useBackend();

    useEffect(() => {


        backend.getPersonalInfo().then((response: any) => {
            if (response === null) {
                throw new Error("No response");
            }
            setPersonalInformation(response);
        });




    }, []);

    return (
        <Dialog>
            <DialogTrigger asChild>
                <Button>Edit Profile</Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <DialogTitle>Edit profile</DialogTitle>
                </DialogHeader>
                <EditInformationForm {...personalInformation}/>
            </DialogContent>
        </Dialog>
    );
}

export default EditInformation;
