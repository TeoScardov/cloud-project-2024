import {
    Menubar,
    MenubarContent,
    MenubarItem,
    MenubarMenu,
    MenubarTrigger,
} from "./components/ui/menubar";

import SheetCart from "./SheetCart";
import { useNavigate } from "react-router-dom";
import {CircleUserRound} from "lucide-react";
import { ModeToggle } from "./ModeToggle";
import { useBackend } from "./services/backendService";
import { useEffect, useState } from "react";


function Navbar() {
    let navigate = useNavigate();
    let backend = useBackend();
    
    const [isAuth, setIsAuth] = useState(false);

    if (localStorage.getItem("token") !== null) {
        backend.getAuth().then((data: any) => {
            if (data.status === 200) {
                setIsAuth(true);
            }
        });
    }

    return (
        <Menubar>
            <MenubarMenu>
                <MenubarTrigger onClick={() => navigate("/")}>
                    eBook Store
                </MenubarTrigger>
            </MenubarMenu>
            <div className="flex-grow"></div>
            <MenubarMenu>
                <MenubarTrigger>
                    <CircleUserRound size={24} />
                </MenubarTrigger>
                {isAuth ? (
                    <MenubarContent>
                        <MenubarItem onClick={() => navigate("/profile")}>
                            Profile
                        </MenubarItem>
                        <MenubarItem
                            onClick={() => {
                                backend.logOut().then(() => {
                                    setIsAuth(false);
                                    backend.token = null;
                                    backend.getHomeBooks(backend.numberOfBooksToDisplay).then(() => {
                                        navigate("/");
                                        window.location.reload();
                                    });
                                    
                                });
                            }}
                        >
                            Log out
                        </MenubarItem>
                    </MenubarContent>
                ) : (
                    <MenubarContent>
                       
                        <MenubarItem onClick={() => navigate("/login")}>
                            Log in
                        </MenubarItem>
                        <MenubarItem onClick={() => navigate("/signup")}>
                            Sign up
                        </MenubarItem>
                    </MenubarContent>
                )}
            </MenubarMenu>
            <MenubarMenu>
                <SheetCart />
            </MenubarMenu>
            <MenubarMenu>
                <ModeToggle />
            </MenubarMenu>
        </Menubar>
    );
}

export default Navbar;
