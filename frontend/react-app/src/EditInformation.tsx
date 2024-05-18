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

function EditInformation(props: PersonInformation) {
    return (
        <Dialog>
            <DialogTrigger asChild>
                <Button>Edit Profile</Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <DialogTitle>Edit profile</DialogTitle>
                </DialogHeader>
                <EditInformationForm {...props} />
            </DialogContent>
        </Dialog>
    );
}

export default EditInformation;
