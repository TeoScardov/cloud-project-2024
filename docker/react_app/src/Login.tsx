import { Button } from "./components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "./components/ui/card"
import LoginForm from "./LoginForm"
import {useNavigate} from "react-router-dom"
import App from "./App"
import { useEffect } from "react"
import { useBackend } from "./services/backendService"

import "./Login.css"


function Login() {

    const navigate = useNavigate()
    const backend = useBackend()


    useEffect(() => {

      if (localStorage.getItem("token") !== null) {
        backend.getAuth().then((response: any) => {
            if (response.status == 200) {
                navigate("/profile");
            } else {
                navigate("/login");
            }
        });
    }

      }, []);

  return (
    <Card className="cardLogin">
      <CardHeader>
        <CardTitle className="text-2xl">Login</CardTitle>
        <CardDescription>
          Enter your email below to login to your account
        </CardDescription>
      </CardHeader>
      <CardContent>
        <LoginForm />
      </CardContent>
    </Card>
  )
}

export default Login;
