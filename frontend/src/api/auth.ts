import axiosInstance from './axios';

export interface LoginRequest {
    email: string;
    password: string;
}

export interface RegisterRequest {
    email: string;
    username: string;
    password: string;
    full_name?: string;
}

export interface TokenResponse {
    access_token: string;
    token_type: string;
    user: {
        id: string;
        email: string;
        username: string;
        full_name?: string;
    };
}

export const authAPI = {
    login: async (data: LoginRequest): Promise<TokenResponse> => {
        const response = await axiosInstance.post('/auth/login', data);
        return response.data;
    },

    register: async (data: RegisterRequest): Promise<TokenResponse> => {
        const response = await axiosInstance.post('/auth/register', data);
        return response.data;
    },

    logout: async (): Promise<void> => {
        await axiosInstance.post('/auth/logout');
    },

    getCurrentUser: async () => {
        const response = await axiosInstance.get('/auth/me');
        return response.data;
    },
};
