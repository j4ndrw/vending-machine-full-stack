import { useSnackbar } from "notistack";
import { useEffect, useState } from "react";
import { register } from "../services/register";
import { Role } from "../types/role";
import SelectRole from "./SelectRole";

function Register() {
    const [username, setUsername] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const [confirmPassword, setConfirmPassword] = useState<string>("");
    const [role, setRole] = useState<Role>();

    const { enqueueSnackbar } = useSnackbar();

    return (
        <div className="m-16">
            <div className="w-full max-w-md m-auto bg-indigo-900 rounded-lg border border-primaryBorder shadow-default py-10 px-16">
                <h1 className="text-2xl font-medium text-primary mt-4 mb-12 text-center">
                    Register
                </h1>

                <form
                    onSubmit={(e) => {
                        e.preventDefault();
                        if (password !== confirmPassword) {
                            enqueueSnackbar("These passwords don't match!", {
                                variant: "error",
                            });
                        } else if (role) {
                            register(username, password, role)
                                .then(({ data, status }) => {
                                    enqueueSnackbar(data.message, {
                                        variant:
                                            status === 200
                                                ? "success"
                                                : "error",
                                    });
                                })
                                .catch(console.error);
                        }
                    }}
                >
                    <div>
                        <label htmlFor="username">Username</label>
                        <input
                            type="username"
                            className={`text-black w-full p-2 text-primary border rounded-md outline-none text-sm transition duration-150 ease-in-out mb-4`}
                            id="username"
                            placeholder="Your Username"
                            onChange={(e) => {
                                setUsername(e.target.value);
                            }}
                        />
                    </div>
                    <div>
                        <label htmlFor="password">Password</label>
                        <input
                            type="password"
                            className={`text-black w-full p-2 text-primary border rounded-md outline-none text-sm transition duration-150 ease-in-out mb-4`}
                            id="password"
                            placeholder="Your Password"
                            onChange={(e) => {
                                setPassword(e.target.value);
                            }}
                        />
                    </div>
                    <div>
                        <label htmlFor="confirmPassword">
                            Confirm Password
                        </label>
                        <input
                            type="password"
                            className={`text-black w-full p-2 text-primary border rounded-md outline-none text-sm transition duration-150 ease-in-out mb-4`}
                            id="confirmPassword"
                            placeholder="Confirm Password"
                            onChange={(e) => {
                                setConfirmPassword(e.target.value);
                            }}
                        />
                    </div>

                    <SelectRole
                        onChange={(e) => setRole(e.target.value as Role)}
                    />

                    <div className="flex justify-center items-center mt-6">
                        <button className="focus:outline-none focus:ring-2 focus:ring-offset-2  focus:ring-purple-400 ml-3 bg-purple-100 transition duration-150 text-gray-600 ease-in-out hover:border-purple-400 hover:bg-purple-300 border rounded px-8 py-2 text-sm">
                            Register
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default Register;
