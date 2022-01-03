export function amountToString(amount) {
    amount = amount.toString().padStart(3, "0");
    return amount.replace(/(.{2})$/, ".$1");
}