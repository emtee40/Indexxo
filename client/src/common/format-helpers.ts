export function formatDate(date: Date): string {

    if (isToday(date)) {
        // Must be formatted like 23:59
        return `${date.getHours()}:${date.getMinutes()}`
    } else if (isSameYear(date)) {
        // Must be formatted like 31 Dec
        return `${date.getDate()} ${date.toLocaleString('default', { month: 'short' })}`
    } else {
        // Must be formatted like 31 Dec 2099
        return `${date.getDate()} ${date.toLocaleString('default', { month: 'short' })} ${date.getFullYear()}`
    }
}

// Copy/Paste from https://gist.github.com/zentala/1e6f72438796d74531803cc3833c039c
export function formatBytes(bytes: number, decimals: number) {
    if (bytes == 0) return '0 Bytes';
    var k = 1024,
        dm = decimals || 2,
        sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
        i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

function isToday(someDate: Date): boolean {
    const today = new Date()
    return someDate.getDate() == today.getDate() &&
        someDate.getMonth() == today.getMonth() &&
        someDate.getFullYear() == today.getFullYear()
}

function isSameYear(someDate: Date): boolean {
    const today = new Date()
    return someDate.getFullYear() == today.getFullYear()
}
