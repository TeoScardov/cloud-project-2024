import {
    Menubar,
    MenubarContent,
    MenubarItem,
    MenubarMenu,
    MenubarSeparator,
    MenubarShortcut,
    MenubarTrigger,
    MenubarSub,
    MenubarSubContent,
    MenubarSubTrigger,
    MenubarCheckboxItem,
    MenubarRadioGroup,
    MenubarRadioItem,
} from "./components/ui/menubar";

import Cart from "./Cart";
import { useNavigate } from "react-router-dom";
import { Menu } from "lucide-react";
import Profile from "./Profile";

function Navbar() {
    let navigate = useNavigate();

    const isAuth = localStorage.getItem("token") !== null;

    return (
        <Menubar>
            <MenubarMenu>
                <MenubarTrigger onClick={() => navigate("/")}>
                    Home
                </MenubarTrigger>
            </MenubarMenu>
            <div className="flex-grow"></div>
            <MenubarMenu>
                <MenubarTrigger>
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="21"
                        height="21"
                        fill="currentColor"
                        className="bi bi-person-fill"
                        viewBox="0 -1 16 16"
                    >
                        <path d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6" />
                    </svg>
                </MenubarTrigger>
                {isAuth ? (
                    <MenubarContent>
                        <MenubarItem onClick={() => navigate("/profile")}>
                            Profile
                        </MenubarItem>
                        <MenubarItem>Library</MenubarItem>
                        <MenubarItem
                            onClick={() => {
                                navigate("/");
                                localStorage.removeItem("token");
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
                <Cart />
            </MenubarMenu>
        </Menubar>
    );
}

export default Navbar;
