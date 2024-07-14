import { useEffect, useState } from "react";
import { CustomerInformation } from "./EditInformationForm";
import { useBackend } from "./services/backendService";

const PersonalInformation = () => {
    const backend = useBackend();

    const [personalInformation, setPersonalInformation] =
        useState<CustomerInformation>({
            name: "",
            billing_address: "",
            phone_number: "",
            email_address: "",
            cc: "",
            expiredate: "",
            cvv: "",
            surname: "",
            username: "",
        });

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
            {/* <h1>Personal Information</h1> */}
            <p>
                <strong>Name:</strong> {personalInformation.name}
            </p>
            <p>
                <strong>Surname:</strong> {personalInformation.surname}
            </p>
            <p>
                <strong>Username:</strong> {personalInformation.username}
            </p>
            <p>
                <strong>Email:</strong> {personalInformation.email_address}
            </p>
            <p>
                <strong>Phone:</strong>{" "}
                {personalInformation.phone_number === null
                    ? "N/A"
                    : personalInformation.phone_number}
            </p>
            <p>
                <strong>Address:</strong>{" "}
                {personalInformation.billing_address === null
                    ? "N/A"
                    : personalInformation.billing_address}
            </p>
            <p>
                <strong>Credit Card:</strong>{" "}
                {personalInformation.cc === null
                    ? "N/A"
                    : "*".repeat(personalInformation.cc.slice(0, -4).length) +
                      personalInformation.cc.slice(-4)}
            </p>
        </div>
    );
};

export default PersonalInformation;
