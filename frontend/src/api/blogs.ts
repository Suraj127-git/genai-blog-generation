import axiosInstance from './axios';

export interface BlogGenerateRequest {
    topic: string;
    language?: string;
    model?: string;
    document_ids?: string[];
}

export interface Blog {
    id: string;
    title: string;
    content: string;
    topic: string;
    topic_category: string;
    language: string;
    status: string;
    generation_time?: number;
    created_at: string;
}

export interface BlogHistoryResponse {
    blogs: Blog[];
    total: number;
    page: number;
    page_size: number;
    total_pages: number;
}

export const blogsAPI = {
    generateBlog: async (data: BlogGenerateRequest): Promise<Blog> => {
        const response = await axiosInstance.post('/blogs/generate', data);
        return response.data;
    },

    getBlogHistory: async (page = 1, pageSize = 10, search?: string, topicCategory?: string): Promise<BlogHistoryResponse> => {
        const params = new URLSearchParams({
            page: page.toString(),
            page_size: pageSize.toString(),
        });
        if (search) params.append('search', search);
        if (topicCategory) params.append('topic_category', topicCategory);

        const response = await axiosInstance.get(`/blogs/history?${params.toString()}`);
        return response.data;
    },

    getBlog: async (blogId: string): Promise<Blog> => {
        const response = await axiosInstance.get(`/blogs/${blogId}`);
        return response.data;
    },

    deleteBlog: async (blogId: string): Promise<void> => {
        await axiosInstance.delete(`/blogs/${blogId}`);
    },

    downloadBlog: async (blogId: string, format: 'pdf' | 'docx'): Promise<Blob> => {
        const response = await axiosInstance.get(`/blogs/${blogId}/download/${format}`, {
            responseType: 'blob',
        });
        return response.data;
    },
};
