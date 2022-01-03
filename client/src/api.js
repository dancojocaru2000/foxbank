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


export async function getaccountlist(token) {
    try {
        const result = await fetch(new URL("/accounts/", baseURL), {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
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

export async function getcurrencies() {
    try {
        const result = await fetch(new URL("/accounts/meta/currencies", baseURL), {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
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

export async function getaccounttypes() {
    try {
        const result = await fetch(new URL("/accounts/meta/account_types", baseURL), {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
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

export async function createaccount(token, name, currency, type) {
    try {
        const result = await fetch(new URL("/accounts/", baseURL), {
            method: "POST",
            body: JSON.stringify({
                customName: name, 
                currency: currency, 
                accountType: type,
            }),
            headers: {
                "Content-Type": "application/json",
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

export async function getnotificationlist(token) {
    try {
        const result = await fetch(new URL("/notifications/", baseURL), {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
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

export async function createnotification(token, body, read) {
    try {
        const result = await fetch(new URL("/notifications/", baseURL), {
            method: "POST",
            body: JSON.stringify({
                body: body, 
                read: read,
            }),
            headers: {
                "Content-Type": "application/json",
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

export async function marknotificationread(token, id) {
    try {
        const result = await fetch(new URL("/notifications/"+id+"/mark_read", baseURL), {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
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

export async function createtransaction(token, otherparty, amount, accountId, description) {
    try {
        const result = await fetch(new URL("/transactions/", baseURL), {
            method: "POST",
            body: JSON.stringify({
                description: description,
                account_id: accountId,
                destination_iban: otherparty, 
                amount: amount, 
            }),
            headers: {
                "Content-Type": "application/json",
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

    
export async function gettransactions(token, id) {
    try {
        const result = await fetch(new URL("/transactions/?account_id="+id, baseURL), {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
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
