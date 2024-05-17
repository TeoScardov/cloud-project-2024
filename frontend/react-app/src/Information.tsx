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
                <strong>Email:</strong> {props.email}
            </p>
            <p>
                <strong>Phone Number:</strong> {props.phone}
            </p>
            <p>
                <strong>Address:</strong> {props.address}
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
