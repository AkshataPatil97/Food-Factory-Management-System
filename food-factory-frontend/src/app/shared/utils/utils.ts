import { RegistrationForm } from "../interface/user";

// Utility function to create the RegistrationForm object
export function createFormData(username: string, email: string, password: string, selectedRole: { name: string }): RegistrationForm {
    let role = selectedRole.name
    return {
        username,
        email,
        password,
        role
    };
}