export function convertDate(dateString: string | Date, onlyDate: boolean = false): string {
    const date = new Date(dateString);
    return onlyDate ? date.toLocaleDateString() : date.toLocaleString();
}