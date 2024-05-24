import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "./components/ui/card";

import "./Signup.css";
import SignupForm from "./SignupForm";

function Signup() {
    return (
        <Card className="cardSignup">
            <CardHeader>
                <CardTitle className="text-xl">Sign Up</CardTitle>
                <CardDescription>
                    Enter your information to create an account
                </CardDescription>
            </CardHeader>
            <CardContent>
             <SignupForm />
            </CardContent>
        </Card>
    );
}

export default Signup;
