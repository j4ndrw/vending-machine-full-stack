import { useSnackbar } from "notistack";
import { useState } from "react";
import { flushSync } from "react-dom";
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
                                flushSync(() => {});
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
                        <button className="focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-700 transition duration-150 ease-in-out hover:bg-indigo-600 bg-indigo-700 rounded text-white px-8 py-2 text-sm">
                            Login
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default Login;
