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

function Navbar() {
    return (
        <Menubar>
            <MenubarMenu>
                <MenubarTrigger>Home</MenubarTrigger>
            </MenubarMenu>
            <div className="flex-grow"></div>
            <MenubarMenu>
                <MenubarTrigger>Profile</MenubarTrigger>
                <MenubarContent>
                    <MenubarItem>Log in</MenubarItem>
                    <MenubarItem>Log out</MenubarItem>
                    <MenubarItem>Sign up</MenubarItem>
                    <MenubarItem>Library</MenubarItem>
                </MenubarContent>
            </MenubarMenu>
            <MenubarMenu>
                <Cart />
            </MenubarMenu>
        </Menubar>
    );
}

export default Navbar;
