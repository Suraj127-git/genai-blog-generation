import React from 'react';
import { Link } from 'react-router-dom';

interface BlogCardProps {
    id: string;
    title: string;
    content: string;
    topic: string;
    topic_category: string;
    created_at: string;
    generation_time?: number;
    language: string;
    onDelete?: (id: string) => void;
}

const BlogCard: React.FC<BlogCardProps> = ({
    id,
    title,
    content,
    topic,
    topic_category,
    created_at,
    generation_time,
    language,
    onDelete,
}) => {
    const handleDelete = (e: React.MouseEvent) => {
        e.preventDefault();
        if (onDelete) {
            onDelete(id);
        }
    };

    return (
        <div className={`card blog-${topic_category} hover:shadow-lg transition-all duration-200 border-2`}>
            <Link to={`/blog/${id}`} className="block">
                <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2 hover:text-primary-600 transition-colors">
                    {title}
                </h3>
                <p className="text-sm text-gray-600 mb-4 line-clamp-3">
                    {content?.substring(0, 150)}...
                </p>
            </Link>

            <div className="flex items-center justify-between text-xs text-gray-500 mb-3">
                <span className="px-2 py-1 bg-white rounded-md font-medium capitalize">
                    {topic_category}
                </span>
                <span>{new Date(created_at).toLocaleDateString()}</span>
            </div>

            <div className="flex items-center justify-between pt-3 border-t border-gray-200">
                <div className="flex items-center gap-2 text-xs text-gray-500">
                    <span className="px-2 py-1 bg-white rounded">🌐 {language}</span>
                    {generation_time && (
                        <span className="px-2 py-1 bg-white rounded">⚡ {generation_time.toFixed(1)}s</span>
                    )}
                </div>
                {onDelete && (
                    <button
                        onClick={handleDelete}
                        className="text-red-600 hover:text-red-700 text-sm font-medium transition-colors"
                    >
                        Delete
                    </button>
                )}
            </div>
        </div>
    );
};

export default BlogCard;
