const baseURL = "https://foxbank-api.extras.dcdevelop.xyz";

export async function login(username, code) {
    try {
        const result = await fetch(new URL("/login/", baseURL), {
            method: "POST",
            body: JSON.stringify({
                username, code,
            }),
            headers: {
                "Content-Type": "application/json"
            },
        });

        return (await result.json());
    } catch (error) {
        return {
            status: "error",
            code: "request/failure"
        }
    }
}


export async function whoami(token) {
    try {
        const result = await fetch(new URL("/login/whoami", baseURL), {
            method: "GET",
            headers: {
                "Authorization": "Bearer " + token,
            },
        });

        return (await result.json());
    } catch (error) {
        return {
            status: "error",
            code: "request/failure"
        }
    }
}

export async function logout(token) {
    try {
        await fetch(new URL("/login/logout", baseURL), {
            method: "POST",
            headers: {
                "Authorization": "Bearer " + token,
            },
        });
    } catch (error) {
        return {
            status: "error",
            code: "request/failure"
        }
    }
}