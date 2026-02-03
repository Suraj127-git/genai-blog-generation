import axiosInstance from './axios';

export interface DocumentUploadResponse {
    id: string;
    filename: string;
    file_type: string;
    file_size: number;
    content_preview?: string;
    uploaded_at: string;
}

export interface DocumentListResponse {
    documents: DocumentUploadResponse[];
    total: number;
}

export const documentsAPI = {
    uploadDocument: async (file: File): Promise<DocumentUploadResponse> => {
        const formData = new FormData();
        formData.append('file', file);

        const response = await axiosInstance.post('/documents/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },

    listDocuments: async (): Promise<DocumentListResponse> => {
        const response = await axiosInstance.get('/documents');
        return response.data;
    },

    getDocument: async (docId: string): Promise<DocumentUploadResponse> => {
        const response = await axiosInstance.get(`/documents/${docId}`);
        return response.data;
    },

    deleteDocument: async (docId: string): Promise<void> => {
        await axiosInstance.delete(`/documents/${docId}`);
    },
};
