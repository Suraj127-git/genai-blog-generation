import { configureStore } from '@reduxjs/toolkit';
import authReducer from '../features/auth/authSlice';
import blogsReducer from '../features/blogs/blogsSlice';
import documentsReducer from '../features/documents/documentsSlice';

export const store = configureStore({
    reducer: {
        auth: authReducer,
        blogs: blogsReducer,
        documents: documentsReducer,
    },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
