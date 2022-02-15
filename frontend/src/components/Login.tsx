import { useSnackbar } from "notistack";
import { useState } from "react";
import { login } from "../services/login";

function Login() {
    const [username, setUsername] = useState<string>("");
    const [password, setPassword] = useState<string>("");

    const { enqueueSnackbar } = useSnackbar();

    return (
        <div className="m-16">
            <div className="w-full max-w-md m-auto bg-indigo-900 rounded-lg border border-primaryBorder shadow-default py-10 px-16">
                <h1 className="text-2xl font-medium text-primary mt-4 mb-12 text-center">
                    Log in to your account
                </h1>

                <form
                    onSubmit={(e) => {
                        e.preventDefault();
                        login(username, password)
                            .then(({ data, status }) => {
                                enqueueSnackbar(data.message, {
                                    variant:
                                        status === 200 ? "success" : "error",
                                });
                            })
                            .catch(console.error);
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

                    <div className="flex justify-center items-center mt-6">
                        <button
                            className={`bg-blue-800 py-2 px-4 text-sm text-white rounded border border-green focus:outline-none focus:border-green-dark`}
                        >
                            Login
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default Login;
