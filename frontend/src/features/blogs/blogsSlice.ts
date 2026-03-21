import { createSlice, createAsyncThunk, type PayloadAction } from '@reduxjs/toolkit';
import { blogsAPI } from '../../api/blogs';
import type { BlogGenerateRequest, Blog, BlogHistoryResponse } from '../../api/blogs';

interface BlogsState {
    currentBlog: Blog | null;
    history: Blog[];
    total: number;
    page: number;
    totalPages: number;
    loading: boolean;
    generating: boolean;
    error: string | null;
}

const initialState: BlogsState = {
    currentBlog: null,
    history: [],
    total: 0,
    page: 1,
    totalPages: 0,
    loading: false,
    generating: false,
    error: null,
};

export const generateBlog = createAsyncThunk(
    'blogs/generate',
    async (data: BlogGenerateRequest, { rejectWithValue }) => {
        try {
            const response = await blogsAPI.generateBlog(data);
            return response;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.detail || 'Blog generation failed');
        }
    }
);

export const fetchBlogHistory = createAsyncThunk(
    'blogs/fetchHistory',
    async ({ page, pageSize, search, topicCategory }: { page?: number; pageSize?: number; search?: string; topicCategory?: string }, { rejectWithValue }) => {
        try {
            const response = await blogsAPI.getBlogHistory(page, pageSize, search, topicCategory);
            return response;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.detail || 'Failed to fetch history');
        }
    }
);

export const fetchBlog = createAsyncThunk(
    'blogs/fetchBlog',
    async (blogId: string, { rejectWithValue }) => {
        try {
            const response = await blogsAPI.getBlog(blogId);
            return response;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.detail || 'Failed to fetch blog');
        }
    }
);

export const deleteBlog = createAsyncThunk(
    'blogs/delete',
    async (blogId: string, { rejectWithValue }) => {
        try {
            await blogsAPI.deleteBlog(blogId);
            return blogId;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.detail || 'Failed to delete blog');
        }
    }
);

const blogsSlice = createSlice({
    name: 'blogs',
    initialState,
    reducers: {
        clearCurrentBlog: (state) => {
            state.currentBlog = null;
        },
        clearError: (state) => {
            state.error = null;
        },
    },
    extraReducers: (builder) => {
        // Generate Blog
        builder.addCase(generateBlog.pending, (state) => {
            state.generating = true;
            state.error = null;
        });
        builder.addCase(generateBlog.fulfilled, (state, action: PayloadAction<Blog>) => {
            state.generating = false;
            state.currentBlog = action.payload;
        });
        builder.addCase(generateBlog.rejected, (state, action) => {
            state.generating = false;
            state.error = action.payload as string;
        });

        // Fetch History
        builder.addCase(fetchBlogHistory.pending, (state) => {
            state.loading = true;
            state.error = null;
        });
        builder.addCase(fetchBlogHistory.fulfilled, (state, action: PayloadAction<BlogHistoryResponse>) => {
            state.loading = false;
            state.history = action.payload.blogs;
            state.total = action.payload.total;
            state.page = action.payload.page;
            state.totalPages = action.payload.total_pages;
        });
        builder.addCase(fetchBlogHistory.rejected, (state, action) => {
            state.loading = false;
            state.error = action.payload as string;
        });

        // Fetch Blog
        builder.addCase(fetchBlog.pending, (state) => {
            state.loading = true;
            state.error = null;
        });
        builder.addCase(fetchBlog.fulfilled, (state, action: PayloadAction<Blog>) => {
            state.loading = false;
            state.currentBlog = action.payload;
        });
        builder.addCase(fetchBlog.rejected, (state, action) => {
            state.loading = false;
            state.error = action.payload as string;
        });

        // Delete Blog
        builder.addCase(deleteBlog.fulfilled, (state, action: PayloadAction<string>) => {
            state.history = state.history.filter(blog => blog.id !== action.payload);
            state.total -= 1;
        });
    },
});

export const { clearCurrentBlog, clearError } = blogsSlice.actions;
export default blogsSlice.reducer;
