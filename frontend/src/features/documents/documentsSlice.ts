import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { documentsAPI, DocumentUploadResponse, DocumentListResponse } from '../../api/documents';

interface DocumentsState {
    documents: DocumentUploadResponse[];
    total: number;
    uploading: false;
    loading: boolean;
    error: string | null;
}

const initialState: DocumentsState = {
    documents: [],
    total: 0,
    uploading: false,
    loading: false,
    error: null,
};

export const uploadDocument = createAsyncThunk(
    'documents/upload',
    async (file: File, { rejectWithValue }) => {
        try {
            const response = await documentsAPI.uploadDocument(file);
            return response;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.detail || 'Upload failed');
        }
    }
);

export const fetchDocuments = createAsyncThunk(
    'documents/fetch',
    async (_, { rejectWithValue }) => {
        try {
            const response = await documentsAPI.listDocuments();
            return response;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.detail || 'Failed to fetch documents');
        }
    }
);

export const deleteDocument = createAsyncThunk(
    'documents/delete',
    async (docId: string, { rejectWithValue }) => {
        try {
            await documentsAPI.deleteDocument(docId);
            return docId;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.detail || 'Failed to delete document');
        }
    }
);

const documentsSlice = createSlice({
    name: 'documents',
    initialState,
    reducers: {
        clearError: (state) => {
            state.error = null;
        },
    },
    extraReducers: (builder) => {
        // Upload
        builder.addCase(uploadDocument.pending, (state) => {
            state.uploading = true;
            state.error = null;
        });
        builder.addCase(uploadDocument.fulfilled, (state, action: PayloadAction<DocumentUploadResponse>) => {
            state.uploading = false;
            state.documents.unshift(action.payload);
            state.total += 1;
        });
        builder.addCase(uploadDocument.rejected, (state, action) => {
            state.uploading = false;
            state.error = action.payload as string;
        });

        // Fetch
        builder.addCase(fetchDocuments.pending, (state) => {
            state.loading = true;
            state.error = null;
        });
        builder.addCase(fetchDocuments.fulfilled, (state, action: PayloadAction<DocumentListResponse>) => {
            state.loading = false;
            state.documents = action.payload.documents;
            state.total = action.payload.total;
        });
        builder.addCase(fetchDocuments.rejected, (state, action) => {
            state.loading = false;
            state.error = action.payload as string;
        });

        // Delete
        builder.addCase(deleteDocument.fulfilled, (state, action: PayloadAction<string>) => {
            state.documents = state.documents.filter(doc => doc.id !== action.payload);
            state.total -= 1;
        });
    },
});

export const { clearError } = documentsSlice.actions;
export default documentsSlice.reducer;
