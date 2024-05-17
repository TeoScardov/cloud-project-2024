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
import {CircleUserRound} from "lucide-react";
import { ModeToggle } from "./ModeToggle";


function Navbar() {
    let navigate = useNavigate();

    const isAuth = localStorage.getItem("token") !== null;

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
            <MenubarMenu>
                <ModeToggle />
            </MenubarMenu>
        </Menubar>
    );
}

export default Navbar;
