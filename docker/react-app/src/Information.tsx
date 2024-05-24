import { useEffect, useState } from "react";
import { CustomerInformation } from "./EditInformationForm";
import { useBackend } from "./services/backendService";

const PersonalInformation = () => {

    const backend = useBackend();

    const [personalInformation, setPersonalInformation] = useState<CustomerInformation | null>(null);

    useEffect(() => {
        backend.getPersonalInfo().then((response: any) => {
            
            if (response === null) {
                throw new Error("No response");
            }

            setPersonalInformation(response);
        });
    }, []);

    return (
        <div
            style={{
                padding: "20px",
                maxWidth: "600px",
            }}
        >
            {personalInformation && (
                <p>
                    <strong>Name:</strong> {personalInformation.name}
                </p>
            )}
            {personalInformation && (
                <p>
                    <strong>Surname:</strong> {personalInformation.surname}
                </p>
            )}
            {personalInformation && (
                <p>
                    <strong>Username:</strong> {personalInformation.username}
                </p>
            )}
            {personalInformation && (
                <p>
                    <strong>Email:</strong> {personalInformation.email_address}
                </p>
            )}
            {personalInformation && (
                <p>
                    <strong>Phone Number:</strong> {personalInformation.phone_number}
                </p>
            )}
            {personalInformation && (
                <p>
                    <strong>Address:</strong> {personalInformation.billing_address}
                </p>
            )}
            {/*             // NOT WORKIN
            {personalInformation && (
                <p>
                    <strong>Credit Card:</strong>{" "}
                    {"*".repeat(personalInformation.cc.slice(0, -4).length) + personalInformation.cc.slice(-4)}
                </p>
            )} */}
        </div>
    );
};

export default PersonalInformation;
