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

import "./Login.css"


function Login() {

    let navigate = useNavigate()

    useEffect(() => {
        if (localStorage.getItem("token")) {
            navigate("/")
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
