import React from "react";
import { PersonInformation } from "./EditInformationForm";

const PersonalInformation = (props: PersonInformation) => {

    return (
        <div
            style={{
                padding: "20px",
                maxWidth: "600px",
            }}
        >
            <p>
                <strong>Name:</strong> {props.name}
            </p>
            <p>
                <strong>Surname:</strong> {props.surname}
            </p>
            <p>
                <strong>Username:</strong> {props.username}
            </p>
            <p>
                <strong>Email:</strong> {props.email_address}
            </p>
            <p>
                <strong>Phone Number:</strong> {props.phone_number}
            </p>
            <p>
                <strong>Address:</strong> {props.billing_address}
            </p>
            <p>
                <strong>Credit Card:</strong>{" "}
                {"*".repeat(props.cc.slice(0, -4).length) + props.cc.slice(-4)}
            </p>
        </div>
    );
};

export default PersonalInformation;
export type { PersonInformation };
