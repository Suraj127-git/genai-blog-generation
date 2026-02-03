import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { authAPI, LoginRequest, RegisterRequest, TokenResponse } from '../../api/auth';

interface User {
    id: string;
    email: string;
    username: string;
    full_name?: string;
}

interface AuthState {
    user: User | null;
    token: string | null;
    isAuthenticated: boolean;
    loading: boolean;
    error: string | null;
}

const initialState: AuthState = {
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    token: localStorage.getItem('token'),
    isAuthenticated: !!localStorage.getItem('token'),
    loading: false,
    error: null,
};

export const login = createAsyncThunk(
    'auth/login',
    async (credentials: LoginRequest, { rejectWithValue }) => {
        try {
            const response = await authAPI.login(credentials);
            return response;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.detail || 'Login failed');
        }
    }
);

export const register = createAsyncThunk(
    'auth/register',
    async (userData: RegisterRequest, { rejectWithValue }) => {
        try {
            const response = await authAPI.register(userData);
            return response;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.detail || 'Registration failed');
        }
    }
);

export const logout = createAsyncThunk('auth/logout', async () => {
    await authAPI.logout();
});

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        clearError: (state) => {
            state.error = null;
        },
    },
    extraReducers: (builder) => {
        // Login
        builder.addCase(login.pending, (state) => {
            state.loading = true;
            state.error = null;
        });
        builder.addCase(login.fulfilled, (state, action: PayloadAction<TokenResponse>) => {
            state.loading = false;
            state.isAuthenticated = true;
            state.token = action.payload.access_token;
            state.user = action.payload.user;
            localStorage.setItem('token', action.payload.access_token);
            localStorage.setItem('user', JSON.stringify(action.payload.user));
        });
        builder.addCase(login.rejected, (state, action) => {
            state.loading = false;
            state.error = action.payload as string;
        });

        // Register
        builder.addCase(register.pending, (state) => {
            state.loading = true;
            state.error = null;
        });
        builder.addCase(register.fulfilled, (state, action: PayloadAction<TokenResponse>) => {
            state.loading = false;
            state.isAuthenticated = true;
            state.token = action.payload.access_token;
            state.user = action.payload.user;
            localStorage.setItem('token', action.payload.access_token);
            localStorage.setItem('user', JSON.stringify(action.payload.user));
        });
        builder.addCase(register.rejected, (state, action) => {
            state.loading = false;
            state.error = action.payload as string;
        });

        // Logout
        builder.addCase(logout.fulfilled, (state) => {
            state.user = null;
            state.token = null;
            state.isAuthenticated = false;
            localStorage.removeItem('token');
            localStorage.removeItem('user');
        });
    },
});

export const { clearError } = authSlice.actions;
export default authSlice.reducer;
