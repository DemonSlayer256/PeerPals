export default function logout()
{
    console.log("Logging out user...");
    localStorage.clear();
    window.location.href = '/';
}